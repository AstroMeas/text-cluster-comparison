from dash import Output, Input, State, callback, html, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash

# Import your cluster analysis functions
from src.preprocessing.text_preprocessing import cluster_preprocess
from src.clustering.cluster_search import find_cluster
from src.clustering.compare import compare_texts

# Callback to analyze texts and create graphs
@callback(
    [Output('main-graph', 'figure'),
     Output('diff-graph', 'figure'),
     Output('cluster-data-store', 'data')],
    [Input('analyze-button', 'n_clicks')],
    [State('text-data-store', 'data'),
     State('cluster-slider', 'value'),
     State('graph-type', 'value')],
    prevent_initial_call=True
)
def analyze_texts(n_clicks, text_data, min_cluster_size, graph_type):
    """
    Analyzes texts and creates cluster visualizations.
    
    Args:
        n_clicks (int): Number of button clicks
        text_data (dict): Text data from store
        min_cluster_size (int): Minimum cluster size
        graph_type (str): Graph type ('Bubble' or 'Line')
        
    Returns:
        tuple: (main_graph, diff_graph, cluster_data)
    """
    if n_clicks <= 0 or not text_data:
        # Return empty figures
        empty_fig = px.scatter(title="No data to display")
        return empty_fig, empty_fig, {}

    # Extract data from store
    text_a = text_data.get('text_a', '')
    text_b = text_data.get('text_b', '')
    title_a = text_data.get('title_a', 'Text A')
    title_b = text_data.get('title_b', 'Text B')
    separators = text_data.get('separators', [])
    replacements = text_data.get('replacements', [])
    
    # Process texts
    processed_a = cluster_preprocess(text_a, separators, replacements)
    processed_b = cluster_preprocess(text_b, separators, replacements)

    # Find clusters
    cluster_df = find_cluster(processed_a, processed_b, min_cluster_size, title_a, title_b)
    
    # Create visualizations
    if graph_type == 'Bubble':
        main_fig = create_bubble_plot(cluster_df, title_a, title_b)
        diff_fig = create_difference_bubble_plot(cluster_df, title_a)
    else:
        main_fig = create_line_plot(cluster_df, title_a, title_b)
        diff_fig = create_difference_line_plot(cluster_df, title_a)
    
    return main_fig, diff_fig, cluster_df.to_dict()

# Callback to update graphs based on type
@callback(
    [Output('main-graph', 'figure', allow_duplicate=True),
     Output('diff-graph', 'figure', allow_duplicate=True)],
    [Input('update-graph-button', 'n_clicks'),
     Input('graph-type', 'value')],
    [State('cluster-data-store', 'data')],
    prevent_initial_call='initial_duplicate'  # Geändert von True zu 'initial_duplicate'
)
def update_graph_type(n_clicks, graph_type, cluster_data):
    """
    Updates graphs based on selected visualization type.
    
    Args:
        n_clicks (int): Number of button clicks
        graph_type (str): Graph type ('Bubble' or 'Line')
        cluster_data (dict): Cluster data from store
        
    Returns:
        tuple: (main_graph, diff_graph)
    """
    if not cluster_data:
        raise dash.exceptions.PreventUpdate
    
    # Convert data back to DataFrame
    cluster_df = pd.DataFrame(cluster_data)
    
    # Create visualizations based on type
    if graph_type == 'Bubble':
        main_fig = create_bubble_plot(cluster_df, title_a=None, title_b=None)
        diff_fig = create_difference_bubble_plot(cluster_df, title_a=None)
    else:
        main_fig = create_line_plot(cluster_df, title_a=None, title_b=None)
        diff_fig = create_difference_line_plot(cluster_df, title_a=None)
    
    return main_fig, diff_fig

# Callback to remove selected clusters
@callback(
    [Output('cluster-data-store', 'data', allow_duplicate=True),
     Output('main-graph', 'figure', allow_duplicate=True),
     Output('diff-graph', 'figure', allow_duplicate=True)],
    [Input('remove-cluster-button', 'n_clicks')],
    [State('main-graph', 'selectedData'),
     State('cluster-data-store', 'data'),
     State('graph-type', 'value')],
    prevent_initial_call='initial_duplicate'  # Geändert von True zu 'initial_duplicate'
)
def remove_selected_clusters(n_clicks, selected_data, cluster_data, graph_type):
    """
    Removes selected clusters from the visualization.
    
    Args:
        n_clicks (int): Number of button clicks
        selected_data (dict): Selected points data from graph
        cluster_data (dict): Cluster data from store
        graph_type (str): Graph type ('Bubble' or 'Line')
        
    Returns:
        tuple: (updated_cluster_data, updated_main_graph, updated_diff_graph)
    """
    if n_clicks <= 0 or not selected_data or not cluster_data:
        raise dash.exceptions.PreventUpdate
    
    # Convert data back to DataFrame
    cluster_df = pd.DataFrame(cluster_data)
    
    # Extract selected points
    selected_points = [point['x'] for point in selected_data['points']]
    
    # Get column names for filtering
    start_a_col = None
    for col in cluster_df.columns:
        if col.startswith('start_'):
            start_a_col = col
            break
    
    if not start_a_col:
        raise dash.exceptions.PreventUpdate
    
    # Filter out selected clusters
    filtered_df = cluster_df[~cluster_df[start_a_col].isin(selected_points)]
    
    # Create updated visualizations
    if graph_type == 'Bubble':
        main_fig = create_bubble_plot(filtered_df, title_a=None, title_b=None)
        diff_fig = create_difference_bubble_plot(filtered_df, title_a=None)
    else:
        main_fig = create_line_plot(filtered_df, title_a=None, title_b=None)
        diff_fig = create_difference_line_plot(filtered_df, title_a=None)
    
    return filtered_df.to_dict(), main_fig, diff_fig

# Callback to generate comparison table
@callback(
    [Output('comparison-table', 'columns'),
     Output('comparison-table', 'data'),
     Output('download-data-store', 'data')],
    [Input('generate-table-button', 'n_clicks')],
    [State('text-data-store', 'data'),
     State('cluster-data-store', 'data')],
    prevent_initial_call=True
)
def generate_comparison_table(n_clicks, text_data, cluster_data):
    """
    Generates a detailed comparison table between texts.
    
    Args:
        n_clicks (int): Number of button clicks
        text_data (dict): Text data from store
        cluster_data (dict): Cluster data from store
        
    Returns:
        tuple: (table_columns, table_data, download_data)
    """
    if n_clicks <= 0 or not text_data or not cluster_data:
        return [], [], {}
    
    # Extract data
    text_a = text_data.get('text_a', '')
    text_b = text_data.get('text_b', '')
    title_a = text_data.get('title_a', 'Text A')
    title_b = text_data.get('title_b', 'Text B')
    separators = text_data.get('separators', [])
    replacements = text_data.get('replacements', [])
    
    # Process texts
    processed_a = cluster_preprocess(text_a, separators, replacements)
    processed_b = cluster_preprocess(text_b, separators, replacements)
    
    # Convert cluster data to DataFrame
    cluster_df = pd.DataFrame(cluster_data)
    
    # Generate comparison table
    comparison_df = compare_texts(processed_a, processed_b, cluster_df, title_a, title_b)
    
    # Format table for Dash
    columns = [{"name": col, "id": col} for col in comparison_df.columns]
    table_data = comparison_df.to_dict('records')
    
    return columns, table_data, comparison_df.to_dict()

# Helper functions for visualizations
def create_bubble_plot(df, title_a=None, title_b=None):
    """Creates a bubble plot for cluster visualization."""
    # Determine column names
    start_a_col = next((col for col in df.columns if col.startswith('start_')), None)
    start_b_col = next((col for col in df.columns if col != start_a_col and col.startswith('start_')), None)
    
    if not start_a_col or not start_b_col or df.empty:
        return px.scatter(title="No data to display")
    
    # Create figure
    fig = px.scatter(
        df, 
        x=start_a_col, 
        y=start_b_col, 
        size='length',
        hover_data=[start_a_col, start_b_col, 'length']
    )
    
    # Set labels
    x_title = title_a if title_a else start_a_col.replace('start_', '')
    y_title = title_b if title_b else start_b_col.replace('start_', '')
    
    fig.update_layout(
        title="Cluster Visualization",
        xaxis_title=x_title,
        yaxis_title=y_title,
        clickmode='event+select'
    )
    
    return fig

def create_difference_bubble_plot(df, title_a=None):
    """Creates a bubble plot showing position differences."""
    # Determine column name
    start_a_col = next((col for col in df.columns if col.startswith('start_')), None)
    
    if not start_a_col or df.empty:
        return px.scatter(title="No data to display")
    
    # Create figure
    fig = px.scatter(
        df, 
        x=start_a_col, 
        y='differenz', 
        size='length',
        hover_data=[start_a_col, 'differenz', 'length']
    )
    
    # Set labels
    x_title = title_a if title_a else start_a_col.replace('start_', '')
    
    fig.update_layout(
        title="Position Difference Visualization",
        xaxis_title=x_title,
        yaxis_title="Position Difference"
    )
    
    return fig

def create_line_plot(df, title_a=None, title_b=None):
    """Creates a line plot connecting cluster start and end points."""
    # Determine column names
    start_a_col = next((col for col in df.columns if col.startswith('start_')), None)
    end_a_col = next((col for col in df.columns if col.startswith('end_') and col.endswith(start_a_col.split('_')[-1])), None)
    start_b_col = next((col for col in df.columns if col != start_a_col and col.startswith('start_')), None)
    end_b_col = next((col for col in df.columns if col.startswith('end_') and col.endswith(start_b_col.split('_')[-1])), None)
    
    if not all([start_a_col, end_a_col, start_b_col, end_b_col]) or df.empty:
        return go.Figure(layout=dict(title="No data to display"))
    
    # Create figure
    fig = go.Figure()
    
    # Add cluster lines
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row[start_a_col], row[end_a_col]],
            y=[row[start_b_col], row[end_b_col]],
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(color='blue', size=5)
        ))
    
    # Add diagonal reference line
    max_val = max(df[end_a_col].max(), df[end_b_col].max()) if not df.empty else 100
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color='grey', width=1),
        showlegend=False
    ))
    
    # Set labels
    x_title = title_a if title_a else start_a_col.replace('start_', '')
    y_title = title_b if title_b else start_b_col.replace('start_', '')
    
    fig.update_layout(
        title="Cluster Visualization",
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=False,
        clickmode='event+select'
    )
    
    return fig

def create_difference_line_plot(df, title_a=None):
    """Creates a line plot showing differences."""
    # Determine column names
    start_a_col = next((col for col in df.columns if col.startswith('start_')), None)
    end_a_col = next((col for col in df.columns if col.startswith('end_') and col.endswith(start_a_col.split('_')[-1])), None)
    
    if not all([start_a_col, end_a_col]) or df.empty:
        return go.Figure(layout=dict(title="No data to display"))
    
    # Create figure
    fig = go.Figure()
    
    # Add cluster lines
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row[start_a_col], row[end_a_col]],
            y=[row['differenz'], row['differenz']],
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(color='blue', size=5)
        ))
    
    # Add zero reference line
    max_val = df[end_a_col].max() if not df.empty else 100
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, 0],
        mode='lines',
        line=dict(color='grey', width=1),
        showlegend=False
    ))
    
    # Set labels
    x_title = title_a if title_a else start_a_col.replace('start_', '')
    
    fig.update_layout(
        title="Position Difference Visualization",
        xaxis_title=x_title,
        yaxis_title="Position Difference",
        showlegend=False
    )
    
    return fig