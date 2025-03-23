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
                html.H1("Texteingabe"),
                html.P(
                    "Geben Sie die zwei zu vergleichenden Texte ein und legen Sie die Vorverarbeitungsoptionen fest."
                ),
                html.Button(
                    "Beispieldaten laden", 
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
                        html.Label("Titel für Text A:"),
                        dcc.Input(
                            id="title-a-input",
                            type="text",
                            placeholder="Geben Sie einen Titel für Text A ein",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Text content input
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Inhalt von Text A:"),
                        html.Div(
                            className="text-area-container",
                            children=[
                                dcc.Textarea(
                                    id="text-a-input",
                                    placeholder="Geben Sie hier den Inhalt von Text A ein...",
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
                        html.Label("Titel für Text B:"),
                        dcc.Input(
                            id="title-b-input",
                            type="text",
                            placeholder="Geben Sie einen Titel für Text B ein",
                            style={"width": "100%"}
                        )
                    ]
                ),
                
                # Text content input
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Inhalt von Text B:"),
                        html.Div(
                            className="text-area-container",
                            children=[
                                dcc.Textarea(
                                    id="text-b-input",
                                    placeholder="Geben Sie hier den Inhalt von Text B ein...",
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
                html.H2("Vorverarbeitungsoptionen"),
                
                # Improved Separator selection 
                html.Div(
                    className="input-section",
                    children=[
                        html.Label("Separatoren:"),
                        html.P(
                            "Wählen Sie die Zeichen aus, die zur Textteilung verwendet werden sollen",
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
                                                {"label": " Punkt (.)", "value": "."},
                                                {"label": " Komma (,)", "value": ","},
                                                {"label": " Semikolon (;)", "value": ";"},
                                                {"label": " Doppelpunkt (:)", "value": ":"},
                                                {"label": " Schrägstrich (/)", "value": "/"},
                                                {"label": " Backslash (\\)", "value": "\\"},
                                                {"label": " Bindestrich (-)", "value": "-"},
                                                {"label": " Leerzeichen", "value": " "},
                                                {"label": " Tabulator", "value": "\t"},
                                                {"label": " Zeilenumbruch", "value": "\n"},
                                            ],
                                            value=[" ", "."],  # Default: Leerzeichen und Punkt
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
                                html.Label("Zusätzliche benutzerdefinierte Separatoren:"),
                                dcc.Input(
                                    id="custom-separators-input",
                                    type="text",
                                    placeholder="z.B.: ? ! # $",
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
                        html.Label("Zeichenersetzungen:"),
                        html.P(
                            "Geben Sie Zeichenersetzungen im Format 'alt:neu' an (durch Komma getrennt)",
                            className="text-muted"
                        ),
                        dcc.Input(
                            id="replacements-input",
                            type="text",
                            placeholder="z.B.: ä:ae,ö:oe,ü:ue",
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
                                html.Label("Schritt 1:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                                html.Button(
                                    "Daten speichern", 
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
                                html.Label("Schritt 2:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                                dcc.Link(
                                    html.Button(
                                        "Zur Analyse gehen", 
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