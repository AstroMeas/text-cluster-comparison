from dash import Output, Input, State, callback, html, dash_table, dcc
import dash
import json

# Import example data functions
from src.text_example.load_example_Notre_dame_wikipedia import load_text_a, load_text_b, example_parameters

# Callback to load example data
@callback(
    [Output('text-a-input', 'value'),
     Output('text-b-input', 'value'),
     Output('separators-input', 'value'),
     Output('title-a-input', 'value'),
     Output('title-b-input', 'value'),
     Output('replacements-input', 'value')],
    [Input('load-example-button', 'n_clicks')],
    prevent_initial_call=True
)
def load_example_data(n_clicks):
    """
    Loads example data into the input fields.
    
    Args:
        n_clicks (int): Number of button clicks
        
    Returns:
        tuple: Text A, Text B, Separators, Title A, Title B, and Replacements
    """
    if n_clicks <= 0:
        return "", "", "", "", "", ""
    
    # Load example texts
    text_a = load_text_a()
    text_b = load_text_b()
    
    # Load example parameters
    separators, replacements, title_a, title_b = example_parameters()
    
    # Format separators
    separator_str = ",".join(separators)
    
    # Format replacements
    if replacements:
        replacement_str = ",".join([f"{old}:{new}" for old, new in replacements])
    else:
        replacement_str = ""
    
    return text_a, text_b, separator_str, title_a, title_b, replacement_str

# Callback to save input data
@callback(
    [Output('text-data-store', 'data'),
     Output('input-status', 'children')],
    [Input('save-input-button', 'n_clicks')],
    [State('text-a-input', 'value'),
     State('text-b-input', 'value'),
     State('title-a-input', 'value'),
     State('title-b-input', 'value'),
     State('separators-input', 'value'),
     State('replacements-input', 'value')],
    prevent_initial_call=True
)
def save_input_data(n_clicks, text_a, text_b, title_a, title_b, separators, replacements):
    """
    Saves input data to the store for use in other pages.
    
    Args:
        n_clicks (int): Number of button clicks
        text_a (str): Text A content
        text_b (str): Text B content
        title_a (str): Title for Text A
        title_b (str): Title for Text B
        separators (str): Comma-separated list of separators
        replacements (str): Comma-separated list of replacements in format "old:new"
        
    Returns:
        tuple: (data_store, status_message)
    """
    if n_clicks <= 0:
        return {}, None
    
    # Validate inputs
    if not text_a or not text_b:
        return {}, html.Div("Error: Both Text A and Text B are required", style={"color": "red"})
    
    # Default titles if not provided
    if not title_a:
        title_a = "Text A"
    if not title_b:
        title_b = "Text B"
    
    # Process separators
    separator_list = []
    if separators:
        separator_list = [s.strip() for s in separators.split(",")]
    
    # Process replacements
    replacement_list = []
    if replacements:
        for r in replacements.split(","):
            parts = r.split(":")
            if len(parts) == 2:
                replacement_list.append((parts[0].strip(), parts[1].strip()))
    
    # Create data store
    data = {
        "text_a": text_a,
        "text_b": text_b,
        "title_a": title_a,
        "title_b": title_b,
        "separators": separator_list,
        "replacements": replacement_list
    }
    
    return data, html.Div("Data saved successfully! You can now proceed to Analysis.", 
                         style={"color": "green"})

# Callback to populate input fields from store
@callback(
    [Output('text-a-input', 'value', allow_duplicate=True),
     Output('text-b-input', 'value', allow_duplicate=True),
     Output('title-a-input', 'value', allow_duplicate=True),
     Output('title-b-input', 'value', allow_duplicate=True),
     Output('separators-input', 'value', allow_duplicate=True),
     Output('replacements-input', 'value', allow_duplicate=True)],
    [Input('url', 'pathname')],
    [State('text-data-store', 'data')],
    prevent_initial_call='initial_duplicate'  # Geändert von True zu 'initial_duplicate'
)
def populate_from_store(pathname, data):
    """
    Populates input fields from store data when navigating to input page.
    
    Args:
        pathname (str): Current URL path
        data (dict): Data from store
        
    Returns:
        tuple: Text A, Text B, Title A, Title B, Separators, Replacements
    """
    if pathname != '/input' or not data:
        raise dash.exceptions.PreventUpdate
    
    # Get values from store
    text_a = data.get('text_a', '')
    text_b = data.get('text_b', '')
    title_a = data.get('title_a', '')
    title_b = data.get('title_b', '')
    
    # Format separators
    separators = ",".join(data.get('separators', []))
    
    # Format replacements
    replacements = ",".join([f"{old}:{new}" for old, new in data.get('replacements', [])])
    
    return text_a, text_b, title_a, title_b, separators, replacements