from dash import Output, Input, State, callback, dcc
import pandas as pd
from src.web.utils.download_utils import prepare_download

# Callback for downloading table data
@callback(
    Output('download-table', 'data'),
    [Input('download-table-button', 'n_clicks')],
    [State('download-data-store', 'data'),
     State('download-format', 'value')],
    prevent_initial_call=True
)
def download_table_data(n_clicks, data, format):
    """
    Prepares the comparison table data for download.
    
    Args:
        n_clicks (int): Number of button clicks
        data (dict): Table data from store
        format (str): Download format ('csv' or 'html')
        
    Returns:
        dict: Download data dictionary
    """
    if n_clicks <= 0 or not data:
        return None
    
    return prepare_download(data, format, 'comparison_table')

# Callback for downloading graph data
@callback(
    Output('download-graph', 'data'),
    [Input('download-graph-button', 'n_clicks')],
    [State('cluster-data-store', 'data'),
     State('download-format', 'value')],
    prevent_initial_call=True
)
def download_graph_data(n_clicks, data, format):
    """
    Prepares the cluster data for download.
    
    Args:
        n_clicks (int): Number of button clicks
        data (dict): Cluster data from store
        format (str): Download format ('csv' or 'html')
        
    Returns:
        dict: Download data dictionary
    """
    if n_clicks <= 0 or not data:
        return None
    
    return prepare_download(data, format, 'cluster_data')