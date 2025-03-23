from dash import Output, Input, State, callback, html

# Callback to update theme and store theme preference
@callback(
    [Output('theme-store', 'data'),
     Output('app-container', 'className')],
    [Input('theme-toggle-switch', 'value')],
    [State('theme-store', 'data')]
)
def toggle_theme(theme_value, theme_data):
    """
    Updates the theme based on toggle switch value.
    
    Args:
        theme_value (str): Selected theme ('light' or 'dark')
        theme_data (dict): Current theme data from store
        
    Returns:
        tuple: (updated_theme_data, app_container_class)
    """
    if theme_data is None:
        theme_data = {'theme': 'light'}
    
    # Update theme in store
    theme_data['theme'] = theme_value
    
    # Set appropriate class for container based on theme
    app_container_class = "app-container dark-mode" if theme_value == 'dark' else "app-container"
    
    return theme_data, app_container_class

# Callback to initialize theme from stored preference
@callback(
    [Output('theme-toggle-switch', 'value'),
     Output('app-container', 'className', allow_duplicate=True)],
    [Input('url', 'pathname')],  # Change: URL as trigger instead of theme-store
    [State('theme-store', 'data')],  # theme-store now as State, not as Input
    prevent_initial_call='initial_duplicate'
)
def initialize_theme(pathname, theme_data):
    """
    Initializes the theme based on stored preference when the page loads.
    
    Args:
        pathname (str): Current URL path (used as trigger)
        theme_data (dict): Theme data from store
        
    Returns:
        tuple: (theme_value, app_container_class)
    """
    # Default to light theme if no data
    if theme_data is None or 'theme' not in theme_data:
        theme_value = 'light'
    else:
        theme_value = theme_data['theme']
    
    # Set appropriate class for container based on theme
    app_container_class = "app-container dark-mode" if theme_value == 'dark' else "app-container"
    
    return theme_value, app_container_class