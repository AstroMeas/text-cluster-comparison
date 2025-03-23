from dash import Output, Input, callback
from src.web.layouts.main_layout import render_page_content

# Callback to update page content based on URL
@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """
    Updates the page content based on the URL path.
    
    Args:
        pathname (str): The current URL path
        
    Returns:
        dash component: The layout for the requested page
    """
    return render_page_content(pathname)

# Callback to update active link class in sidebar
@callback(
    [Output('welcome-link', 'className'),
     Output('input-link', 'className'),
     Output('analysis-link', 'className')],
    [Input('url', 'pathname')]
)
def set_active_link(pathname):
    """
    Updates the active class for sidebar links based on the current page.
    
    Args:
        pathname (str): The current URL path
        
    Returns:
        tuple: (welcome_class, input_class, analysis_class) with active class for current page
    """
    welcome_class = "sidebar-link active" if pathname == '/' or pathname == '/welcome' else "sidebar-link"
    input_class = "sidebar-link active" if pathname == '/input' else "sidebar-link"
    analysis_class = "sidebar-link active" if pathname == '/analysis' else "sidebar-link"
    
    return welcome_class, input_class, analysis_class