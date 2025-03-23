from dash import html, dcc

# Import layouts
from .sidebar import create_sidebar
from .welcome_layout import create_welcome_layout
from .input_layout import create_input_layout  
from .analysis_layout import create_analysis_layout

def create_main_layout():
    """
    Creates the main layout for the application that includes:
    - Sidebar for navigation
    - Content area that changes based on URL
    - Global data stores for sharing data between pages
    
    Returns:
        html.Div: The main application layout
    """
    return html.Div(
        className="app-container",
        id="app-container",
        children=[
            # Store components for sharing data between pages
            dcc.Store(id='theme-store', storage_type='local', data={'theme': 'light'}),
            dcc.Store(id='text-data-store', storage_type='session'),
            dcc.Store(id='cluster-data-store', storage_type='session'),
            dcc.Store(id='download-data-store', storage_type='memory'),
            
            # URL location for multi-page navigation
            dcc.Location(id='url', refresh=False),
            
            # Sidebar with navigation links
            create_sidebar(),
            
            # Main content area that changes based on URL
            html.Div(
                id='page-content',
                className='content-container',
                children=[]
            )
        ]
    )

def render_page_content(pathname):
    """
    Renders the correct page content based on the URL pathname.
    
    Args:
        pathname (str): The URL path
        
    Returns:
        dash component: The layout for the requested page
    """
    # Default page is welcome
    if pathname == '/' or pathname == '/welcome':
        return create_welcome_layout()
    
    # Input page for text preprocessing
    elif pathname == '/input':
        return create_input_layout()
    
    # Analysis page for cluster visualization
    elif pathname == '/analysis':
        return create_analysis_layout()
    
    # 404 page for undefined routes
    else:
        return html.Div(
            className="content-card",
            children=[
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized...")
            ]
        )