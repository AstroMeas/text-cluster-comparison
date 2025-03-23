from dash import html, dcc
from src.web.layouts.theme_toggle import create_theme_toggle

def create_sidebar():
    """
    Creates the sidebar navigation component with links to different pages.
    
    Returns:
        html.Div: The sidebar component
    """
    return html.Div(
        className="sidebar",
        children=[
            # App title
            html.Div(
                className="sidebar-header",
                children=["Text Cluster Comparison"]
            ),
            
            # Navigation links
            html.Ul(
                className="sidebar-nav",
                children=[
                    html.Li(
                        dcc.Link(
                            "Welcome",
                            href="/welcome",
                            className="sidebar-link",
                            id="welcome-link"
                        )
                    ),
                    html.Li(
                        dcc.Link(
                            "Text Input",
                            href="/input",
                            className="sidebar-link",
                            id="input-link"
                        )
                    ),
                    html.Li(
                        dcc.Link(
                            "Analysis",
                            href="/analysis",
                            className="sidebar-link",
                            id="analysis-link"
                        )
                    )
                ]
            ),
            
            # Theme toggle component
            create_theme_toggle()
        ]
    )