import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, Input, Output, State

# Import necessary functions (adjust paths according to your actual structure)
from src.clustering.cluster_search import find_cluster
from src.preprocessing.text_preprocessing import cluster_preprocess

# Analyze texts and create initial graphs
@callback(
    Output('graph', 'figure', allow_duplicate=True),
    Output('graph_diff', 'figure', allow_duplicate=True),
    Output('store_df', 'data', allow_duplicate=True),
    Input('start_button', 'n_clicks'),
    State('text_a_input', 'value'),
    State('text_b_input', 'value'),
    State('seperators', 'value'),
    State('cluster_slider', 'value'),
    State('graph_type', 'value'),
    State('title_a_input', 'value'),
    State('title_b_input', 'value'),
    prevent_initial_call=True
)
def update_graph(clicks, text_a, text_b, seps, min_clus, plot_type, title_a, title_b):
    """
    Analyzes texts and creates visualization graphs.
    
    Args:
        clicks: Number of button clicks
        text_a: First text content
        text_b: Second text content
        seps: Separator characters
        min_clus: Minimum cluster size
        plot_type: Type of plot (Bubble or Line)
        title_a: Name of the first text
        title_b: Name of the second text
        
    Returns:
        tuple: Main graph figure, difference graph figure, and cluster data
    """
    if clicks >= 1:
        # Process input separators
        sep_list = seps.split(',') if seps else []
        
        # Preprocess texts
        processed_a = cluster_preprocess(text_a, sep_list)
        processed_b = cluster_preprocess(text_b, sep_list)
        
        # Find clusters
        cluster_df = find_cluster(processed_a, processed_b, int(min_clus), title_a, title_b)
        
        # Create visualizations based on the chosen type
        if plot_type == 'Bubble':
            fig1 = create_bubble_plot(cluster_df, title_a, title_b)
            fig2 = create_difference_bubble_plot(cluster_df, title_a)
        else:
            fig1 = create_line_plot(cluster_df, title_a, title_b)
            fig2 = create_difference_line_plot(cluster_df, title_a)
        
        return fig1, fig2, cluster_df.to_dict()
    
    # Return empty plots if not clicked
    return px.scatter(), px.scatter(), {}

# Update existing graphs based on type change
@callback(
    Output('graph', 'figure', allow_duplicate=True),
    Output('graph_diff', 'figure', allow_duplicate=True),
    Input('graph_type', 'value'),
    Input('update_g_button', 'n_clicks'),
    State('store_df', 'data'),
    State('title_a_input', 'value'),
    State('title_b_input', 'value'),
    prevent_initial_call=True
)
def update_graph_type(plot_type, clicks, cluster_df, title_a, title_b):
    """
    Updates graph type without reprocessing texts.
    
    Args:
        plot_type: Type of plot (Bubble or Line)
        clicks: Number of button clicks
        cluster_df: Cluster data
        title_a: Name of the first text
        title_b: Name of the second text
        
    Returns:
        tuple: Main graph figure, difference graph figure
    """
    # Convert back to DataFrame
    cluster_df = pd.DataFrame(cluster_df)
    
    # Create visualizations based on the chosen type
    if plot_type == 'Bubble':
        fig1 = create_bubble_plot(cluster_df, title_a, title_b)
        fig2 = create_difference_bubble_plot(cluster_df, title_a)
    else:
        fig1 = create_line_plot(cluster_df, title_a, title_b)
        fig2 = create_difference_line_plot(cluster_df, title_a)
    
    return fig1, fig2

# Helper functions for creating plots
def create_bubble_plot(df, title_a, title_b):
    """Creates a bubble plot showing clusters."""
    fig = px.scatter(df, x=f'start_{title_a}', y=f'start_{title_b}', size='length')
    fig.update_layout(clickmode='event+select')
    return fig

def create_difference_bubble_plot(df, title_a):
    """Creates a bubble plot showing position differences."""
    return px.scatter(df, x=f'start_{title_a}', y='differenz', size='length')

def create_line_plot(df, title_a, title_b):
    """Creates a line plot connecting cluster start and end points."""
    fig = go.Figure()
    
    # Add cluster lines
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row[f'start_{title_a}'], row[f'end_{title_a}']],
            y=[row[f'start_{title_b}'], row[f'end_{title_b}']],
            mode='lines+markers',
            name=f"Line {row.name}",
            line=dict(color='blue', width=2),
            marker=dict(color='blue', size=5)
        ))
    
    # Add diagonal reference line
    max_val = max(df[f'end_{title_a}'].max(), df[f'end_{title_b}'].max()) if not df.empty else 100
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color='grey', width=1),
        name='y = x',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title="Cluster Visualization",
        xaxis_title=f'{title_a}',
        yaxis_title=f"{title_b}",
        showlegend=False,
    )
    
    return fig

def create_difference_line_plot(df, title_a):
    """Creates a line plot showing differences."""
    fig = go.Figure()
    
    # Add cluster lines
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row[f'start_{title_a}'], row[f'end_{title_a}']],
            y=[row['differenz'], row['differenz']],
            mode='lines+markers',
            name=f"Line {row.name}",
            line=dict(color='blue', width=2),
            marker=dict(color='blue', size=5)
        ))
    
    # Add zero reference line
    max_val = df[f'end_{title_a}'].max() if not df.empty else 100
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, 0],
        mode='lines',
        line=dict(color='grey', width=1),
        name='y = 0',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title="Difference Visualization",
        xaxis_title=f'{title_a}',
        yaxis_title="Position Difference",
        showlegend=False,
    )
    
    return fig