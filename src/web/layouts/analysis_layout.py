from dash import html, dcc, dash_table

def create_analysis_layout():
    """
    Creates the analysis page layout with cluster visualization and controls.
    
    Returns:
        html.Div: The analysis page layout
    """
    return html.Div([
        # Header and controls
        html.Div(
            className="content-card",
            children=[
                html.H1("Text Analysis"),
                html.P("Analyze text similarities and visualize clusters."),
                html.Div(
                    style={"display": "flex", "align-items": "center", "gap": "20px", "margin-top": "20px"},
                    children=[
                        html.Div(
                            style={"flex": "1"},
                            children=[
                                html.Label("Minimum Cluster Size:"),
                                dcc.Slider(
                                    min=1, max=50, step=1, value=10,
                                    id="cluster-slider",
                                    marks=None,
                                    tooltip={"placement": "bottom", "always_visible": True},
                                )
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Label("Visualization Type:"),
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Bubble", "value": "Bubble"},
                                        {"label": "Line", "value": "Line"}
                                    ],
                                    value="Bubble",
                                    id="graph-type"
                                )
                            ]
                        ),
                        html.Button(
                            "Analyze Texts", 
                            id="analyze-button",
                            className="app-button",
                            n_clicks=0
                        )
                    ]
                )
            ]
        ),
        
        # Visualization section
        html.Div(
            className="content-card",
            children=[
                html.H2("Cluster Visualization"),
                
                # Graphs
                html.Div(
                    className="graph-container",
                    children=[
                        html.Div(
                            className="graph-item",
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=[
                                        dcc.Graph(
                                            id="main-graph",
                                            config={"displayModeBar": True}
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className="graph-item",
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=[
                                        dcc.Graph(
                                            id="diff-graph",
                                            config={"displayModeBar": True}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Graph controls
                html.Div(
                    style={"display": "flex", "gap": "10px", "margin-top": "20px"},
                    children=[
                        html.Button(
                            "Remove Selected Clusters", 
                            id="remove-cluster-button",
                            className="app-button",
                            n_clicks=0
                        ),
                        html.Button(
                            "Update Graph", 
                            id="update-graph-button",
                            className="app-button",
                            n_clicks=0
                        )
                    ]
                )
            ]
        ),
        
        # Comparison table section
        html.Div(
            
            className="content-card",
            children=[
                html.H2("Detailed Comparison"),
                    html.Div(style={"display": "flex", "gap": "10px", "margin-top": "20px"},
                            children=[
                    html.Button(
                        "Generate Comparison Table", 
                        id="generate-table-button",
                        className="app-button",
                        style={"margin-bottom": "20px"},
                        n_clicks=0
                    ),
                    dcc.Checklist(['Enforce Rising Cluster Order'],
                                ['Enforce Rising Cluster Order'],
                                id='enforce-rising-cluster-order'),
                    
                    # Data table
                    dcc.Loading(
                        type="circle",
                        children=[
                            dash_table.DataTable(
                                id="comparison-table",
                                style_header={
                                    'backgroundColor': 'var(--sidebar-bg)', 
                                    'fontWeight': 'bold',
                                    'color': 'var(--text-color)'
                                },
                                style_cell={
                                    'backgroundColor': 'var(--card-bg)',
                                    'color': 'var(--text-color)',
                                    'textAlign': 'left',
                                    'minWidth': '20px', 
                                    'maxWidth': '400px', 
                                    'width': 'auto'
                                },
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto'
                                },
                                page_size=10
                            )
                        ]
                    )
                ]
                )
            ]
        
        ),
        
        # Download section
        html.Div(
            className="content-card",
            children=[
                html.H2("Download Results"),
                
                html.Div(
                    style={"display": "flex", "align-items": "center", "gap": "20px"},
                    children=[
                        html.Label("Download Format:"),
                        dcc.RadioItems(
                            options=[
                                {"label": "CSV", "value": "csv"},
                                {"label": "HTML", "value": "html"}
                            ],
                            value="html",
                            id="download-format"
                        )
                    ]
                ),
                
                html.Div(
                    style={"display": "flex", "gap": "10px", "margin-top": "20px"},
                    children=[
                        html.Button(
                            "Download Table Data", 
                            id="download-table-button",
                            className="app-button",
                            n_clicks=0
                        ),
                        html.Button(
                            "Download Graph Data", 
                            id="download-graph-button",
                            className="app-button",
                            n_clicks=0
                        )
                    ]
                ),
                
                # Download components
                dcc.Download(id="download-table"),
                dcc.Download(id="download-graph")
            ]
        )
    ])