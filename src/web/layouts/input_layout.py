from dash import html, dcc

def create_input_layout():
    """
    Creates the text input page layout for entering and preprocessing texts.
    
    Returns:
        html.Div: The text input page layout
    """
    return html.Div([
        # Header and instructions
        html.Div(
            className="content-card",
            children=[
                html.H1("Text Input"),
                html.P(
                    "Enter the two texts you want to compare and set preprocessing options."
                ),
                html.Button(
                    "Load Example Data", 
                    id="load-example-button",
                    className="app-button",
                    n_clicks=0
                )
            ]
        ),
        
        # Text A input section
        html.Div(
            className="content-card",
            children=[
                html.H2("Text A"),
                
                # Title input
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Title for Text A:"),
                        dcc.Input(
                            id="title-a-input",
                            type="text",
                            placeholder="Enter a title for Text A",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Text content input
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Text A Content:"),
                        html.Div(
                            className="text-area-container",
                            children=[
                                dcc.Textarea(
                                    id="text-a-input",
                                    placeholder="Enter Text A content here...",
                                    style={"width": "100%", "height": "200px"}
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        
        # Text B input section
        html.Div(
            className="content-card",
            children=[
                html.H2("Text B"),
                
                # Title input
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Title for Text B:"),
                        dcc.Input(
                            id="title-b-input",
                            type="text",
                            placeholder="Enter a title for Text B",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Text content input
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Text B Content:"),
                        html.Div(
                            className="text-area-container",
                            children=[
                                dcc.Textarea(
                                    id="text-b-input",
                                    placeholder="Enter Text B content here...",
                                    style={"width": "100%", "height": "200px"}
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        
        # Preprocessing options
        html.Div(
            className="content-card",
            children=[
                html.H2("Preprocessing Options"),
                
                # Separators
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Separators:"),
                        html.P(
                            "Specify characters that should be used to split the text (comma-separated)",
                            className="text-muted"
                        ),
                        dcc.Input(
                            id="separators-input",
                            type="text",
                            placeholder="E.g.: , . ; : - space",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Character replacements
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Character Replacements:"),
                        html.P(
                            "Specify character replacements in format 'old:new' (comma-separated)",
                            className="text-muted"
                        ),
                        dcc.Input(
                            id="replacements-input",
                            type="text",
                            placeholder="E.g.: ä:ae,ö:oe,ü:ue",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Save button
                html.Div(
                    style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"},
                    children=[
                        html.Button(
                            "Save Input Data", 
                            id="save-input-button",
                            className="app-button",
                            n_clicks=0
                        ),
                        
                        dcc.Link(
                            html.Button(
                                "Proceed to Analysis", 
                                className="app-button",
                            ),
                            href="/analysis"
                        )
                    ]
                ),
                
                # Status message
                html.Div(id="input-status", style={"margin-top": "10px"})
            ]
        )
    ])