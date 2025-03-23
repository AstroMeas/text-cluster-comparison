from dash import Output, Input, State, callback, html, dash_table, dcc
import dash
import json

# Import example data functions
from src.text_example.load_example_Notre_dame_wikipedia import load_text_a, load_text_b, example_parameters

# Callback to combine selected separators
@callback(
    Output('separators-input', 'data'),
    [Input('common-separators', 'value'),
     Input('custom-separators-input', 'value')]
)
def combine_separators(common_seps, custom_seps):
    """
    Combines selected common separators with custom separators.
    
    Args:
        common_seps (list): List of selected common separators
        custom_seps (str): Custom additional separators
        
    Returns:
        str: Combined separator string (comma-separated)
    """
    # Ensure we're working with a list
    separators = list(common_seps) if common_seps else []
    
    # Add custom separators if provided
    if custom_seps:
        # Extract individual characters (if user separates them with commas or spaces)
        custom_chars = [c.strip() for c in custom_seps.replace(',', ' ').split() if c.strip()]
        separators.extend(custom_chars)
    
    # Debug: Print actual values
    print(f"Combined separators before joining: {repr(separators)}")
    
    # We'll use a special marker for space to avoid losing it in string operations
    result = []
    for sep in separators:
        if sep == " ":
            result.append("SPACE")
        else:
            result.append(sep)
            
    # Return as comma-separated string
    return ",".join(result)

# Callback to load example data
@callback(
    [Output('text-a-input', 'value'),
     Output('text-b-input', 'value'),
     Output('common-separators', 'value'),
     Output('custom-separators-input', 'value'),
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
        tuple: Text A, Text B, Common Separators, Custom Separators, Title A, Title B, and Replacements
    """
    if n_clicks <= 0:
        return "", "", [], "", "", "", ""
    
    # Load example texts
    text_a = load_text_a()
    text_b = load_text_b()
    
    # Load example parameters
    separators, replacements, title_a, title_b = example_parameters()
    
    # Debug output
    print(f"Example separators: {repr(separators)}")
    
    # Split separators into common and custom
    common_seps = []
    custom_seps = []
    
    # Standard separators that we support in the UI
    standard_seps = [".", ",", ";", ":", "/", "\\", "-", " ", "\t", "\n"]
    
    for sep in separators:
        if sep in standard_seps:
            common_seps.append(sep)
        else:
            custom_seps.append(sep)
    
    # Ensure space is included
    if " " not in common_seps:
        common_seps.append(" ")
        
    custom_seps_str = " ".join(custom_seps)
    
    # Debug output
    print(f"Common separators: {repr(common_seps)}")
    print(f"Custom separators: {repr(custom_seps_str)}")
    
    # Format replacements
    if replacements:
        replacement_str = ",".join([f"{old}:{new}" for old, new in replacements])
    else:
        replacement_str = ""
    
    return text_a, text_b, common_seps, custom_seps_str, title_a, title_b, replacement_str

# Callback to save input data
@callback(
    [Output('text-data-store', 'data'),
     Output('input-status', 'children')],
    [Input('save-input-button', 'n_clicks')],
    [State('text-a-input', 'value'),
     State('text-b-input', 'value'),
     State('title-a-input', 'value'),
     State('title-b-input', 'value'),
     State('separators-input', 'data'),
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
    
    # Process separators with special handling for space
    separator_list = []
    if separators:
        for sep in separators.split(","):
            sep = sep.strip()
            if sep == "SPACE":
                separator_list.append(" ")  # Convert back to space
            elif sep:  # Skip empty strings
                separator_list.append(sep)
    
    # Always ensure space is included
    if " " not in separator_list:
        separator_list.append(" ")
    
    # Debug output
    print(f"Final separator list: {repr(separator_list)}")
    
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
    
    return data, html.Div("Data successfully saved! You can now proceed to the analysis.", 
                         style={"color": "green"})

# Callback to populate input fields from store
@callback(
    [Output('text-a-input', 'value', allow_duplicate=True),
     Output('text-b-input', 'value', allow_duplicate=True),
     Output('title-a-input', 'value', allow_duplicate=True),
     Output('title-b-input', 'value', allow_duplicate=True),
     Output('common-separators', 'value', allow_duplicate=True),
     Output('custom-separators-input', 'value', allow_duplicate=True),
     Output('replacements-input', 'value', allow_duplicate=True)],
    [Input('url', 'pathname')],
    [State('text-data-store', 'data')],
    prevent_initial_call='initial_duplicate'
)
def populate_from_store(pathname, data):
    """
    Populates input fields from store data when navigating to input page.
    
    Args:
        pathname (str): Current URL path
        data (dict): Data from store
        
    Returns:
        tuple: Text A, Text B, Title A, Title B, Common Separators, Custom Separators, Replacements
    """
    if pathname != '/input' or not data:
        raise dash.exceptions.PreventUpdate
    
    # Get values from store
    text_a = data.get('text_a', '')
    text_b = data.get('text_b', '')
    title_a = data.get('title_a', '')
    title_b = data.get('title_b', '')
    separators = data.get('separators', [])
    
    # Split separators into common and custom
    common_separators = []
    custom_separators = []
    
    standard_seps = [".", ",", ";", ":", "/", "\\", "-", " ", "\t", "\n"]
    
    for sep in separators:
        if sep in standard_seps:
            common_separators.append(sep)
        else:
            custom_separators.append(sep)
    
    custom_separators_str = " ".join(custom_separators)
    
    # Format replacements
    replacements = ",".join([f"{old}:{new}" for old, new in data.get('replacements', [])])
    
    return text_a, text_b, title_a, title_b, common_separators, custom_separators_str, replacements