from dash import html

def create_welcome_layout():
    """
    Creates the welcome page layout with instructions for using the application.
    
    Returns:
        html.Div: The welcome page layout
    """
    return html.Div([
        html.Div(
            className="content-card",
            children=[
                html.H1("Welcome to Text Cluster Comparison"),
                html.P("This tool helps you analyze and find similar text passages between two documents."),
                html.Hr(),
                
                html.H2("How to use this application"),
                
                html.H3("Step 1: Text Input"),
                html.P([
                    "Navigate to the ",
                    html.Strong("Text Input"),
                    " page to enter your two texts. You can also:"
                ]),
                html.Ul([
                    html.Li("Give each text a descriptive title"),
                    html.Li("Specify separators for text tokenization (e.g., comma, period, spaces)"),
                    html.Li("Define character replacements for text normalization")
                ]),
                
                html.H3("Step 2: Analysis"),
                html.P([
                    "After entering your texts, go to the ",
                    html.Strong("Analysis"),
                    " page to visualize the text similarities:"
                ]),
                html.Ul([
                    html.Li("Adjust the minimum cluster size to filter results"),
                    html.Li("View cluster visualizations in bubble or line format"),
                    html.Li("Remove unwanted clusters"),
                    html.Li("Generate a detailed comparison table"),
                    html.Li("Download results in CSV or HTML format")
                ]),
                
                html.H3("Features"),
                html.Ul([
                    html.Li("Automatic identification of similar text passages"),
                    html.Li("Visualization of text similarities"),
                    html.Li("Text preprocessing options"),
                    html.Li("Interactive filtering of results"),
                    html.Li("Export functionality")
                ]),
                
                html.H3("Example Data"),
                html.P([
                    "You can load example data to see how the application works. Click the ",
                    html.Strong("Load Example Data"),
                    " button on the Text Input page."
                ]),
                
                html.Hr(),
                html.P([
                    "Ready to start? Navigate to the ",
                    html.A("Text Input", href="/input", className="text-primary"),
                    " page to begin."
                ])
            ]
        )
    ])