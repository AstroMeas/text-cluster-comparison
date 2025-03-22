from dash import callback, Input, Output, State, dcc

# Import download utilities
from utils.download_utils import download_df

# Download table data callback
@callback(
    Output('download_1', 'data'),
    Input('download_table_button', 'n_clicks'),
    State('download_df', 'data'),
    State('download_format', 'value'),
    prevent_initial_call=True
)
def download_table_data(n_clicks, data, format):
    """
    Downloads the table data in the specified format.
    
    Args:
        n_clicks: Number of button clicks
        data: Data to download
        format: Download format (html or csv)
        
    Returns:
        dict or None: Download data dictionary or None if no data to download
    """
    return download_df(n_clicks, data, format, 'table_data')

# Download graph data callback
@callback(
    Output('download_2', 'data'),
    Input('download_graph_button', 'n_clicks'),
    State('store_df', 'data'),
    State('download_format', 'value'),
    prevent_initial_call=True
)
def download_graph_data(n_clicks, data, format):
    """
    Downloads the graph data in the specified format.
    
    Args:
        n_clicks: Number of button clicks
        data: Data to download
        format: Download format (html or csv)
        
    Returns:
        dict or None: Download data dictionary or None if no data to download
    """
    return download_df(n_clicks, data, format, 'graph_data')