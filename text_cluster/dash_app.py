import pandas as pd
import numpy as np
import datetime
import json

from load_example_text import *
from cluster_functions_nb import *

from dash import Dash, html, dcc, Input, Output, callback,State
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go


def download_df(n_clicks,data,format,filename):
    if not data:
        return None
    
    if format == 'html':
        df = pd.DataFrame(data)
        # **CSS-Styling für HTML-Tabelle definieren**
        style = """
        <style>
            table { width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; }
            th { background-color: lightgrey; font-weight: bold; text-align: left; padding: 8px; }
            td { min-width: 20px; max-width: 400px; word-wrap: break-word; padding: 8px; border: 1px solid #ddd; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:hover { background-color: #ddd; }
        </style>
        """

        # **Pandas Styler für HTML-Tabelle**
        html_table = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', 'lightgrey'), ('font-weight', 'bold'), ('text-align', 'left')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('min-width', '20px'), ('max-width', '400px'), ('word-wrap', 'break-word')]},
            {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
            {'selector': 'tr:hover', 'props': [('background-color', '#ddd')]}
        ]).to_html()

        # **HTML-Datei mit Styling**
        html_content = f"{style}\n{html_table}"

        return dict(content=html_content, filename=f"{filename}.html", type="text/html")
    
    elif format == 'csv':
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, f"{filename}.csv", index=False)
    
    else:
        return None





cluster_df = pd.DataFrame()
comparison_df = pd.DataFrame()
prevent_initial_callbacks='initial_duplicate'

edition_comparison = Dash(__name__)

edition_comparison.layout = html.Div([
    html.H3(children='Edition comparison - cluster finder', style={'textAlign': 'center'}),
    dcc.Store(id='store_df'),
    dcc.Store(id='download_df'),
    html.Button('example_Data',id='load_example',n_clicks=0),

    html.Div([
        # Wrapper Div für die beiden Textbereiche
        html.Div([
            html.Div([dcc.Markdown(children=f'Text A title', id='md_a', style={'width': '20%'}),
            dcc.Textarea(id='title_a_input', style={'width': '70%', 'height': 20})
            ], style={'display': 'flex', 'align-items': 'center', 'width': '100%'}),
            
            dcc.Textarea(id='text_a_input', style={'width': '90%', 'height': 100}),
            dcc.Input(id='seperators',placeholder="all seperators (z. B.: ',', '|', ';')", 
                style={'width': '90%','height':20}),
            
            html.Div('minimal cluster size', id='slider_head', style={'margin-right': '10px'}),  # Text mit Abstand
               
            dcc.Slider(
                    0, 50, 1, value=10, id='cluster_slider',
                    tooltip={"placement": "bottom", "always_visible": True}, marks=None 
                    ),
            dcc.RadioItems(['Bubble','Line'],value='Bubble',id='graph_type')

            ], style={'width': '45%'}),

            html.Div([
                html.Div([dcc.Markdown(children=f'Text b title', id='md_b', style={'width': '20%'}),
                dcc.Textarea(id='title_b_input', style={'width': '70%', 'height': 20})
                ], style={'display': 'flex', 'align-items': 'center', 'width': '100%'}),
                dcc.Textarea(id='text_b_input', style={'width': '90%', 'height': 100}),
                html.Button('Analyze',id='start_button', style={'width': '20%', 'height': 40},n_clicks=0)
                ], style={'width': '45%'}),
            html.Div([],id='loading')
        
        ], style={'display': 'flex'}),
        html.Div([
                html.Div([
                    dcc.Loading([
                    dcc.Graph(id='graph')],id='loading1')
                ], style={'width': '45%'}),

                html.Div([
                    dcc.Loading([
                    dcc.Graph(id='graph_diff')],id='loading2')
                ], style={'width': '45%'})
                
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}
                ),
        html.Div([
                html.Button('Remove Cluster', id='remove', n_clicks=0),
                html.Button('Update Graph', id='update_g_button', n_clicks=0),
                html.Button('Update Table', id='update_table', n_clicks=0)
        ]),
        html.Div([
                dcc.Markdown('Download Format'),
                dcc.RadioItems(['csv', 'html'],'html', id='download_format'),
                html.Button('Download Table', id='download_table_button', n_clicks=0),
                html.Button('Download Graph data', id='download_graph_button', n_clicks=0),
                dcc.Download('download_1'),dcc.Download('download_2')
        ]),
        html.Div([
            dash_table.DataTable(
                id='table',
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left','minWidth': '20px', 'maxWidth': '400px', 'width': 'auto'},
                style_data={'whiteSpace': 'normal','height': 'auto'}  # Automatische Höhe für mehrere Zeilen
            )
        ])
])
# remove selected data
@callback(
        Output('store_df','data',allow_duplicate=True),
        Input('remove','n_clicks'),
        State('graph','selectedData'),
        State('store_df','data'),
        State('title_a_input','value'),
        prevent_initial_call=True
)
def get_click(click,remove_data, df_data, title_a):
    remove_lst = [i['x'] for i in remove_data['points']]
    df = pd.DataFrame(df_data)
    df = df[~df[f'start_{title_a}'].isin(remove_lst)]
    return df.to_dict()

@callback(
    Output('text_a_input','value',allow_duplicate=True),
    Output('text_b_input','value',allow_duplicate=True),
    Output('seperators','value',allow_duplicate=True),
    Output('title_a_input','value',allow_duplicate=True),
    Output('title_b_input','value',allow_duplicate=True),
    Input('load_example','n_clicks'),
    prevent_initial_call=True
)
def load_example(click):
    if click >=1:
        text_a = load_text_a()
        text_b = load_text_b()
        seperators_1,a,b,c = debther_parameters()
        
        seps = r""
        for i in seperators_1:
            seps += ""
            seps += i+","
        return text_a, text_b, seps, b, c
    else:
        return '','','','',''

# Analyse and create graph
@callback(
    Output('graph','figure', allow_duplicate=True),
    Output('graph_diff','figure', allow_duplicate=True),
    Output('store_df','data',allow_duplicate=True),
    Input('start_button','n_clicks'),
    State('text_a_input','value'),
    State('text_b_input','value'),
    State('seperators','value'),
    State('cluster_slider','value'),
    State('graph_type','value'),
    State('title_a_input','value'),
    State('title_b_input','value'),
    prevent_initial_call=True
)
def update_graph(clicks,text_a,text_b,seps,min_clus,type, title_a, title_b):
    if clicks >= 1:
        seps = seps.split(',')

        text_a = clean(text_a,seps) 
        text_b = clean(text_b,seps)    

        cluster_df = find_cluster(text_a,text_b,int(min_clus),title_a, title_b)
        if type == 'Bubble':
            fig1 = px.scatter(cluster_df, x=f'start_{title_a}', y=f'start_{title_b}', size='length')
            fig1.update_layout(clickmode='event+select')
            fig2 = px.scatter(cluster_df, x=f'start_{title_a}', y='differenz', size='length')
        else:
            fig1 = go.Figure()
            for _, row in cluster_df.iterrows():
                fig1.add_trace(go.Scatter(
                x=[row[f'start_{title_a}'], row[f'end_{title_a}']],  # X-Koordinaten
                y=[row[f'start_{title_b}'], row[f'end_{title_b}']],  # Y-Koordinaten
                mode='lines+markers',  # Zeigt Linien und Marker
                name=f"Line {row.name}",  # Optionale Beschriftung
                line=dict(color='blue',width=2),  # Linienbreite
                marker=dict(color='blue',size=5)  # Markierungsgröße
                ))
                fig1.update_layout(
                    title="Linien-Visualisierung basierend auf DataFrame",
                    xaxis_title=f'{title_a}',
                    yaxis_title=f"{title_b}",
                    showlegend=False,  # Legende anzeigen
                    )
                fig1.add_trace(go.Scatter(
                    x=[0, max(cluster_df[f'end_{title_a}'].max(), cluster_df[f'end_{title_b}'].max())],  # Bereich für die Diagonale
                    y=[0, max(cluster_df[f'end_{title_a}'].max(), cluster_df[f'end_{title_b}'].max())],  # y=x
                    mode='lines',  # Nur Linie
                    line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                    name='y = x',  # Beschriftung der Linie
                    showlegend=False  # Keine Legende
                ))
            fig2 = go.Figure()
            for _, row in cluster_df.iterrows():
                fig2.add_trace(go.Scatter(
                x=[row[f'start_{title_a}'], row[f'end_{title_a}']],  # X-Koordinaten
                y=[row['differenz'], row['differenz']],  # Y-Koordinaten
                mode='lines+markers',  # Zeigt Linien und Marker
                name=f"Line {row.name}",  # Optionale Beschriftung
                line=dict(color='blue',width=2),  # Linienbreite
                marker=dict(color='blue',size=5)  # Markierungsgröße
                ))
                fig1.update_layout(
                    title="Linien-Visualisierung basierend auf DataFrame",
                    xaxis_title=f"{title_a}",
                    yaxis_title=f"{title_b}",
                    showlegend=False,  # Legende anzeigen
                    )
                fig1.add_trace(go.Scatter(
                    x=[0, max(cluster_df[f'end_{title_a}'].max(), cluster_df[f'end_{title_b}'].max())],  # Bereich für die Diagonale
                    y=[0, 0],  # y=x
                    mode='lines',  # Nur Linie
                    line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                    name='y = x',  # Beschriftung der Linie
                    showlegend=False  # Keine Legende
                ))
        
        cluster_df = cluster_df.to_dict()
        return fig1, fig2, cluster_df
    
    else:
        return px.scatter(),px.scatter(),cluster_df

# only change type of graph
@callback(
    Output('graph','figure', allow_duplicate=True),
    Output('graph_diff','figure', allow_duplicate=True),
    Input('graph_type','value'),
    Input('update_g_button', 'n_clicks'),
    State('store_df','data'),
    State('title_a_input','value'),
    State('title_b_input','value'),
    prevent_initial_call=True
)
def update_graph(type,clicks,cluster_df,title_a, title_b):
    cluster_df = pd.DataFrame(cluster_df)
    if type == 'Bubble':
        fig1 = px.scatter(cluster_df, x=f'start_{title_a}', y=f'start_{title_b}', size=f'length')
        fig1.update_layout(clickmode='event+select')
        fig2 = px.scatter(cluster_df, x=f'start_{title_a}', y='differenz', size='length')
    else:
        fig1 = go.Figure()
        for _, row in cluster_df.iterrows():
            fig1.add_trace(go.Scatter(
            x=[row[f'start_{title_a}'], row[f'end_{title_a}']],  # X-Koordinaten
            y=[row[f'start_{title_b}'], row[f'end_{title_b}']],  # Y-Koordinaten
            mode='lines+markers',  # Zeigt Linien und Marker
            name=f"Line {row.name}",  # Optionale Beschriftung
            line=dict(color='blue',width=2),  # Linienbreite
            marker=dict(color='blue',size=5)  # Markierungsgröße
            ))
            fig1.update_layout(
                title="Linien-Visualisierung basierend auf DataFrame",
                xaxis_title=f"{title_a}",
                yaxis_title=f"Text_{title_b}",
                showlegend=False,  # Legende anzeigen
                )
            fig1.add_trace(go.Scatter(
                x=[0, max(cluster_df[f'end_{title_a}'].max(), cluster_df[f'end_{title_b}'].max())],  # Bereich für die Diagonale
                y=[0, max(cluster_df[f'end_{title_a}'].max(), cluster_df[f'end_{title_b}'].max())],  # y=x
                    mode='lines',  # Nur Linie
                    line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                    name='y = x',  # Beschriftung der Linie
                    showlegend=False  # Keine Legende
                ))
        fig2 = go.Figure()
        for _, row in cluster_df.iterrows():
            fig2.add_trace(go.Scatter(
                x=[row[f'start_{title_a}'], row[f'end_{title_a}']],  # X-Koordinaten
                y=[row['differenz'], row['differenz']],  # Y-Koordinaten
                mode='lines+markers',  # Zeigt Linien und Marker
                name=f"Line {row.name}",  # Optionale Beschriftung
                line=dict(color='blue',width=2),  # Linienbreite
                marker=dict(color='blue',size=5)  # Markierungsgröße
                ))
            fig2.update_layout(
                    title="Linien-Visualisierung basierend auf DataFrame",
                    xaxis_title=f"{title_a}",
                    yaxis_title=f"{title_b}",
                    showlegend=False,  # Legende anzeigen
                    )
            fig2.add_trace(go.Scatter(
                    x=[0, max(cluster_df[f'end_{title_a}'].max(), cluster_df[f'end_{title_b}'].max())],  # Bereich für die Diagonale
                    y=[0, 0],  # y=x
                    mode='lines',  # Nur Linie
                    line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                    name='y = x',  # Beschriftung der Linie
                    showlegend=False  # Keine Legende
                ))
    
    return fig1, fig2




 # update_table   
@callback(
    Output('table','columns',allow_duplicate=True),
    Output('table','data',allow_duplicate=True),
    Output('download_df','data',allow_duplicate=True),
    Input('update_table','n_clicks'),
    State('store_df','data'),
    State('text_a_input','value'),
    State('text_b_input','value'),
    State('seperators','value'),
    State('title_a_input','value'),
    State('title_b_input','value'),
    prevent_initial_call='initial_duplicate'
)
def update_table(click,data,text_a,text_b,sep,title_a,title_b):
    if data is not None:
        pass
        df = pd.DataFrame(data)
        text_a = clean(text_a,sep) 
        text_b = clean(text_b,sep) 
        df = compare_texts(text_a, text_b, df, title_a, title_b)
        columns = [{"name": col, "id": col} for col in df.keys()]
        return columns,df.to_dict('records'),df.to_dict()
    return [{'name': 'tag', 'id': 'tag'}, {'name': 'Pos_a', 'id': 'Pos_a'}, {'name': 'Length_a', 'id': 'Length_a'}, {'name': 'a', 'id': 'a'}, {'name': 'Pos_b', 'id': 'Pos_b'}, {'name': 'Length_b', 'id': 'Length_b'}, {'name': 'b', 'id': 'b'}, {'name': 'Length_Cluster', 'id': 'Length_Cluster'}, {'name': 'Cluster', 'id': 'Cluster'}], None,pd.DataFrame().to_dict()

@callback(
    Output('download_1','data'),
    Input('download_table_button','n_clicks'),
    State('download_df','data'),
    State('download_format','value'),
    prevent_initial_callback=True
)
def download(n_clicks,data, format):
    return download_df(n_clicks,data,format,'table_data')

# download store_df
@callback(
    Output('download_2','data'),
    Input('download_graph_button','n_clicks'),
    State('store_df','data'),
    State('download_format','value'),
    prevent_initial_callback=True
)
def download(n_clicks,data, format):
    return download_df(n_clicks,data,format,'graph_data')

def run_app(host='127.0.0.1'):
    edition_comparison.run(debug=False, jupyter_mode="external", port=8050,host=host)

if __name__ == '__main__':
    run_app()