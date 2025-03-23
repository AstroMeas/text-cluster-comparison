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
                    "Enter the two texts to compare and set the preprocessing options."
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
                        html.Label("Content of Text A:"),
                        html.Div(
                            className="text-area-container",
                            children=[
                                dcc.Textarea(
                                    id="text-a-input",
                                    placeholder="Enter the content of Text A here...",
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
                        html.Label("Content of Text B:"),
                        html.Div(
                            className="text-area-container",
                            children=[
                                dcc.Textarea(
                                    id="text-b-input",
                                    placeholder="Enter the content of Text B here...",
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
                
                # Improved Separator selection 
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Separators:"),
                        html.P(
                            "Select the characters to be used for text tokenization",
                            className="text-muted"
                        ),
                        
                        # Common separators as checkboxes
                        html.Div(
                            style={"display": "flex", "flex-wrap": "wrap", "gap": "10px", "margin-bottom": "15px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "align-items": "center", "margin-right": "15px"},
                                    children=[
                                        dcc.Checklist(
                                            id="common-separators",
                                            options=[
                                                {"label": " Period (.)", "value": "."},
                                                {"label": " Comma (,)", "value": ","},
                                                {"label": " Semicolon (;)", "value": ";"},
                                                {"label": " Colon (:)", "value": ":"},
                                                {"label": " Forward Slash (/)", "value": "/"},
                                                {"label": " Backslash (\\)", "value": "\\"},
                                                {"label": " Hyphen (-)", "value": "-"},
                                                {"label": " Space", "value": " "},
                                                {"label": " Tab", "value": "\t"},
                                                {"label": " Line Break", "value": "\n"},
                                            ],
                                            value=[" ", "."],  # Default: Space and period
                                            inline=True,
                                            style={"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "5px"}
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        
                        # Custom separators
                        html.Div(
                            children=[
                                html.Label("Additional custom separators:"),
                                dcc.Input(
                                    id="custom-separators-input",
                                    type="text",
                                    placeholder="e.g.: ? ! # $",
                                    style={"width": "100%"}
                                )
                            ]
                        ),
                        
                        # Hidden field to store combined separators
                        dcc.Store(id="separators-input", data="")
                    ]
                ),
                
                # Character replacements
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Character Replacements:"),
                        html.P(
                            "Enter character replacements in 'old:new' format (separated by commas)",
                            className="text-muted"
                        ),
                        dcc.Input(
                            id="replacements-input",
                            type="text",
                            placeholder="e.g.: ä:ae,ö:oe,ü:ue",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Save button section with clearer instructions
                html.Div(
                    style={"display": "flex", "margin-top": "20px", "align-items": "left"},
                    children=[
                        # Step 1: Save data
                        html.Div(
                            style={"display": "flex", "flex-direction": "column", "align-items": "flex-start"},
                            children=[
                                html.Label("Step 1:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                                html.Button(
                                    "Save Data", 
                                    id="save-input-button",
                                    className="app-button",
                                    n_clicks=0
                                )
                            ]
                        ),
                        
                        # Arrow between steps
                        html.Div(
                            "→",
                            style={"font-size": "24px", "margin": "0 20px"}
                        ),
                        
                        # Step 2: Navigate to analysis
                        html.Div(
                            style={"display": "flex", "flex-direction": "column", "align-items": "flex-start"},
                            children=[
                                html.Label("Step 2:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                                dcc.Link(
                                    html.Button(
                                        "Go to Analysis", 
                                        className="app-button",
                                    ),
                                    href="/analysis"
                                )
                            ]
                        )
                    ]
                ),
                
                # Status message
                html.Div(id="input-status", style={"margin-top": "15px"})
            ]
        )
    ])