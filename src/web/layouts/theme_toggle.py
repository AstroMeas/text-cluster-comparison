from dash import html, dcc

def create_theme_toggle():
    """
    Creates a toggle switch for changing between light and dark theme.
    
    Returns:
        html.Div: The theme toggle component
    """
    return html.Div(
        className="theme-toggle",
        children=[
            # Toggle switch
            dcc.RadioItems(
                id='theme-toggle-switch',
                options=[
                    {'label': 'Light', 'value': 'light'},
                    {'label': 'Dark', 'value': 'dark'}
                ],
                value='light',
                inline=True,
                labelStyle={'margin-right': '10px'}
            )
        ]
    )