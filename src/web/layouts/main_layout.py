from dash import html, dcc, dash_table

def create_layout():
    """
    Creates the main layout for the Dash application.
    
    Returns:
        html.Div: The main layout container for the application
    """
    return html.Div([
        html.H3(children='Edition comparison - cluster finder', style={'textAlign': 'center'}),
        dcc.Store(id='store_df'),
        dcc.Store(id='download_df'),
        html.Button('example_Data', id='load_example', n_clicks=0),

        html.Div([
            # Wrapper Div für die beiden Textbereiche
            html.Div([
                html.Div([
                    dcc.Markdown(children=f'Text A title', id='md_a', style={'width': '20%'}),
                    dcc.Textarea(id='title_a_input', style={'width': '70%', 'height': 20})
                ], style={'display': 'flex', 'align-items': 'center', 'width': '100%'}),
                
                dcc.Textarea(id='text_a_input', style={'width': '90%', 'height': 100}),
                dcc.Input(id='seperators', placeholder="all seperators (z. B.: ',', '|', ';')", 
                    style={'width': '90%', 'height': 20}),
                
                html.Div('minimal cluster size', id='slider_head', style={'margin-right': '10px'}),
                
                dcc.Slider(
                        0, 50, 1, value=10, id='cluster_slider',
                        tooltip={"placement": "bottom", "always_visible": True}, marks=None 
                        ),
                dcc.RadioItems(['Bubble', 'Line'], value='Bubble', id='graph_type')

                ], style={'width': '45%'}),

                html.Div([
                    html.Div([
                        dcc.Markdown(children=f'Text b title', id='md_b', style={'width': '20%'}),
                        dcc.Textarea(id='title_b_input', style={'width': '70%', 'height': 20})
                    ], style={'display': 'flex', 'align-items': 'center', 'width': '100%'}),
                    dcc.Textarea(id='text_b_input', style={'width': '90%', 'height': 100}),
                    html.Button('Analyze', id='start_button', style={'width': '20%', 'height': 40}, n_clicks=0)
                ], style={'width': '45%'}),
                html.Div([], id='loading')
            
            ], style={'display': 'flex'}),
            
            html.Div([
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='graph')
                    ], id='loading1')
                ], style={'width': '45%'}),

                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='graph_diff')
                    ], id='loading2')
                ], style={'width': '45%'})
                
            ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}),
            
            html.Div([
                html.Button('Remove Cluster', id='remove', n_clicks=0),
                html.Button('Update Graph', id='update_g_button', n_clicks=0),
                html.Button('Update Table', id='update_table', n_clicks=0)
            ]),
            
            html.Div([
                dcc.Markdown('Download Format'),
                dcc.RadioItems(['csv', 'html'], 'html', id='download_format'),
                html.Button('Download Table', id='download_table_button', n_clicks=0),
                html.Button('Download Graph data', id='download_graph_button', n_clicks=0),
                dcc.Download('download_1'), dcc.Download('download_2')
            ]),
            
            html.Div([
                dash_table.DataTable(
                    id='table',
                    style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left', 'minWidth': '20px', 'maxWidth': '400px', 'width': 'auto'},
                    style_data={'whiteSpace': 'normal', 'height': 'auto'}  # Automatische Höhe für mehrere Zeilen
                )
            ])
    ])