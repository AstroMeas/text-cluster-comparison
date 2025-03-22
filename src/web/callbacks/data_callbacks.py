import pandas as pd
from dash import callback, Input, Output, State

# Import necessary functions (adjust paths according to your actual structure)
from src.clustering.compare import compare_texts
from src.preprocessing.text_preprocessing import cluster_preprocess
from src.text_example.load_example_Notre_dame_wikipedia import load_text_a, load_text_b, example_parameters

# Prevent initial callbacks from triggering automatically
prevent_initial_callbacks = 'initial_duplicate'

# Remove selected clusters
@callback(
    Output('store_df', 'data', allow_duplicate=True),
    Input('remove', 'n_clicks'),
    State('graph', 'selectedData'),
    State('store_df', 'data'),
    State('title_a_input', 'value'),
    prevent_initial_call=True
)
def get_click(click, remove_data, df_data, title_a):
    """
    Removes selected clusters from the dataset.
    
    Args:
        click: Number of button clicks
        remove_data: Selected data points from the graph
        df_data: Current data in the store
        title_a: Name of the first text
        
    Returns:
        dict: Updated data dictionary with selected points removed
    """
    remove_lst = [i['x'] for i in remove_data['points']]
    df = pd.DataFrame(df_data)
    df = df[~df[f'start_{title_a}'].isin(remove_lst)]
    return df.to_dict()

# Load example data
@callback(
    Output('text_a_input', 'value', allow_duplicate=True),
    Output('text_b_input', 'value', allow_duplicate=True),
    Output('seperators', 'value', allow_duplicate=True),
    Output('title_a_input', 'value', allow_duplicate=True),
    Output('title_b_input', 'value', allow_duplicate=True),
    Input('load_example', 'n_clicks'),
    prevent_initial_call=True
)
def load_example_data(click):
    """
    Loads example data when the button is clicked.
    
    Args:
        click: Number of button clicks
        
    Returns:
        tuple: Example text A, text B, separators, title A, title B
    """
    if click >= 1:
        text_a = load_text_a()
        text_b = load_text_b()
        seperators_1, _, title_a, title_b = example_parameters()
        
        seps = r""
        for i in seperators_1:
            seps += i + ","
            
        return text_a, text_b, seps, title_a, title_b
    else:
        return '', '', '', '', ''

# Update table
@callback(
    Output('table', 'columns', allow_duplicate=True),
    Output('table', 'data', allow_duplicate=True),
    Output('download_df', 'data', allow_duplicate=True),
    Input('update_table', 'n_clicks'),
    State('store_df', 'data'),
    State('text_a_input', 'value'),
    State('text_b_input', 'value'),
    State('seperators', 'value'),
    State('title_a_input', 'value'),
    State('title_b_input', 'value'),
    prevent_initial_call='initial_duplicate'
)
def update_table(click, data, text_a, text_b, sep, title_a, title_b):
    """
    Updates the data table based on the current dataset.
    
    Args:
        click: Number of button clicks
        data: Current data in the store
        text_a: First text content
        text_b: Second text content
        sep: Separator characters
        title_a: Name of the first text
        title_b: Name of the second text
        
    Returns:
        tuple: Table columns, table data, and download data
    """
    if data is not None:
        df = pd.DataFrame(data)
        
        # Clean/process texts
        seps = sep.split(',') if sep else []
        processed_a = cluster_preprocess(text_a, seps)
        processed_b = cluster_preprocess(text_b, seps)
        
        # Compare texts
        df = compare_texts(processed_a, processed_b, df, title_a, title_b)
        
        # Format for display
        columns = [{"name": col, "id": col} for col in df.keys()]
        return columns, df.to_dict('records'), df.to_dict()
    
    # Default empty table structure
    return [
        {'name': 'tag', 'id': 'tag'}, 
        {'name': 'Pos_a', 'id': 'Pos_a'}, 
        {'name': 'Length_a', 'id': 'Length_a'}, 
        {'name': 'a', 'id': 'a'}, 
        {'name': 'Pos_b', 'id': 'Pos_b'}, 
        {'name': 'Length_b', 'id': 'Length_b'}, 
        {'name': 'b', 'id': 'b'}, 
        {'name': 'Length_Cluster', 'id': 'Length_Cluster'}, 
        {'name': 'Cluster', 'id': 'Cluster'}
    ], None, pd.DataFrame().to_dict()