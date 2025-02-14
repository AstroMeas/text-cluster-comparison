import pandas as pd
import numpy as np
import datetime
import json

from text_cluster.load_example_text import *
from cluster_functions_nb import *

from dash import Dash, html, dcc, Input, Output, callback,State
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go

def run_app():
    edition_comparison = Dash(__name__)

    edition_comparison.layout = html.Div([
        html.H1(children='Edition comparison - cluster finder', style={'textAlign': 'center'}),
        dcc.Store(id='store_df'),
        dcc.Store(id='download_df'),
        html.Button('example_Data',id='load_example',n_clicks=0),

        html.Div([
            # Wrapper Div für die beiden Textbereiche
            html.Div([
                dcc.Markdown(children=f'Text A', id='md_a', style={'width': '100%'}),
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
                    dcc.Markdown(children=f'Text B', id='md_b', style={'width': '100%'}),
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
                    html.Button('Update Table', id='update_table', n_clicks=0),
                    html.Button('Download Data', id='download_button', n_clicks=0),
                    dcc.Download('download')
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
            prevent_initial_call=True
    )
    def get_click(click,remove_data, df_data):
        remove_lst = [i['x'] for i in remove_data['points']]
        df = pd.DataFrame(df_data)
        df = df[~df['start_a'].isin(remove_lst)]
        return df.to_dict()



    @callback(
        Output('text_a_input','value'),
        Output('text_b_input','value'),
        Output('seperators','value'),
        Input('load_example','n_clicks'),
        prevent_initial_call=True
    )
    def load_example(click):
        if click >=1:
            text_a = debther_gangtok()#[:30000]
            text_b = debther_peking()#[:30000]
            seperators_1,a,b,c = debther_parameters()
            print(seperators_1)
            seps = r""
            for i in seperators_1:
                seps += ""
                seps += i+","
            return text_a,text_b,seps
        else:
            return '','',''

    # Analyse and create graph
    @callback(
        Output('graph','figure', allow_duplicate=True),
        Output('graph_diff','figure', allow_duplicate=True),
        Output('store_df','data'),
        State('text_a_input','value'),
        State('text_b_input','value'),
        State('seperators','value'),
        State('cluster_slider','value'),
        State('graph_type','value'),
        Input('start_button','n_clicks'),
        prevent_initial_call=True
    )
    def update_graph(text_a,text_b,seps,min_clus,type,clicks):
        if clicks >= 1:
            seps = seps.split(',')

            text_a = clean(text_a,seps) 
            text_b = clean(text_b,seps)    

            cluster_df = find_cluster(text_a,text_b,int(min_clus),'a','b')
            if type == 'Bubble':
                fig1 = px.scatter(cluster_df, x='start_a', y='start_b', size='length')
                fig1.update_layout(clickmode='event+select')
                fig2 = px.scatter(cluster_df, x='start_a', y='differenz', size='length')
            else:
                fig1 = go.Figure()
                for _, row in cluster_df.iterrows():
                    fig1.add_trace(go.Scatter(
                    x=[row['start_a'], row['end_a']],  # X-Koordinaten
                    y=[row['start_b'], row['end_b']],  # Y-Koordinaten
                    mode='lines+markers',  # Zeigt Linien und Marker
                    name=f"Line {row.name}",  # Optionale Beschriftung
                    line=dict(color='blue',width=2),  # Linienbreite
                    marker=dict(color='blue',size=5)  # Markierungsgröße
                    ))
                    fig1.update_layout(
                        title="Linien-Visualisierung basierend auf DataFrame",
                        xaxis_title="Text_a",
                        yaxis_title="Text_b",
                        showlegend=False,  # Legende anzeigen
                        )
                    fig1.add_trace(go.Scatter(
                        x=[0, max(cluster_df['end_a'].max(), cluster_df['end_b'].max())],  # Bereich für die Diagonale
                        y=[0, max(cluster_df['end_a'].max(), cluster_df['end_b'].max())],  # y=x
                        mode='lines',  # Nur Linie
                        line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                        name='y = x',  # Beschriftung der Linie
                        showlegend=False  # Keine Legende
                    ))
                fig2 = go.Figure()
                for _, row in cluster_df.iterrows():
                    fig2.add_trace(go.Scatter(
                    x=[row['start_a'], row['end_a']],  # X-Koordinaten
                    y=[row['differenz'], row['differenz']],  # Y-Koordinaten
                    mode='lines+markers',  # Zeigt Linien und Marker
                    name=f"Line {row.name}",  # Optionale Beschriftung
                    line=dict(color='blue',width=2),  # Linienbreite
                    marker=dict(color='blue',size=5)  # Markierungsgröße
                    ))
                    fig1.update_layout(
                        title="Linien-Visualisierung basierend auf DataFrame",
                        xaxis_title="Text_a",
                        yaxis_title="Text_b",
                        showlegend=False,  # Legende anzeigen
                        )
                    fig1.add_trace(go.Scatter(
                        x=[0, max(cluster_df['end_a'].max(), cluster_df['end_b'].max())],  # Bereich für die Diagonale
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
        prevent_initial_call=True
    )
    def update_graph(type,clicks,cluster_df):
        cluster_df = pd.DataFrame(cluster_df)
        if type == 'Bubble':
            fig1 = px.scatter(cluster_df, x='start_a', y='start_b', size='length')
            fig1.update_layout(clickmode='event+select')
            fig2 = px.scatter(cluster_df, x='start_a', y='differenz', size='length')
        else:
            fig1 = go.Figure()
            for _, row in cluster_df.iterrows():
                fig1.add_trace(go.Scatter(
                x=[row['start_a'], row['end_a']],  # X-Koordinaten
                y=[row['start_b'], row['end_b']],  # Y-Koordinaten
                mode='lines+markers',  # Zeigt Linien und Marker
                name=f"Line {row.name}",  # Optionale Beschriftung
                line=dict(color='blue',width=2),  # Linienbreite
                marker=dict(color='blue',size=5)  # Markierungsgröße
                ))
                fig1.update_layout(
                    title="Linien-Visualisierung basierend auf DataFrame",
                    xaxis_title="Text_a",
                    yaxis_title="Text_b",
                    showlegend=False,  # Legende anzeigen
                    )
                fig1.add_trace(go.Scatter(
                    x=[0, max(cluster_df['end_a'].max(), cluster_df['end_b'].max())],  # Bereich für die Diagonale
                    y=[0, max(cluster_df['end_a'].max(), cluster_df['end_b'].max())],  # y=x
                        mode='lines',  # Nur Linie
                        line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                        name='y = x',  # Beschriftung der Linie
                        showlegend=False  # Keine Legende
                    ))
            fig2 = go.Figure()
            for _, row in cluster_df.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[row['start_a'], row['end_a']],  # X-Koordinaten
                    y=[row['differenz'], row['differenz']],  # Y-Koordinaten
                    mode='lines+markers',  # Zeigt Linien und Marker
                    name=f"Line {row.name}",  # Optionale Beschriftung
                    line=dict(color='blue',width=2),  # Linienbreite
                    marker=dict(color='blue',size=5)  # Markierungsgröße
                    ))
                fig2.update_layout(
                        title="Linien-Visualisierung basierend auf DataFrame",
                        xaxis_title="Text_a",
                        yaxis_title="Text_b",
                        showlegend=False,  # Legende anzeigen
                        )
                fig2.add_trace(go.Scatter(
                        x=[0, max(cluster_df['end_a'].max(), cluster_df['end_b'].max())],  # Bereich für die Diagonale
                        y=[0, 0],  # y=x
                        mode='lines',  # Nur Linie
                        line=dict(color='grey', width=1),  # Rote gestrichelte Linie
                        name='y = x',  # Beschriftung der Linie
                        showlegend=False  # Keine Legende
                    ))
        
        return fig1, fig2
        
        
    @callback(
        Output('table','columns'),
        Output('table','data'),
        Output('download_df','data'),
        Input('update_table','n_clicks'),
        State('store_df','data'),
        State('text_a_input','value'),
        State('text_b_input','value'),
        State('seperators','value'),
        prevent_initial_callback=True
    )
    def update_table(click,data,text_a,text_b,sep):
        if data is not None:
            pass
            df = pd.DataFrame(data)
            text_a = clean(text_a,sep) 
            text_b = clean(text_b,sep) 
            df = compare_texts(text_a,text_b,df)
            columns = [{"name": col, "id": col} for col in df.keys()]
            return columns,df.to_dict('records'),df.to_dict()
        return [{'name': 'tag', 'id': 'tag'}, {'name': 'Pos_a', 'id': 'Pos_a'}, {'name': 'Length_a', 'id': 'Length_a'}, {'name': 'a', 'id': 'a'}, {'name': 'Pos_b', 'id': 'Pos_b'}, {'name': 'Length_b', 'id': 'Length_b'}, {'name': 'b', 'id': 'b'}, {'name': 'Length_Cluster', 'id': 'Length_Cluster'}, {'name': 'Cluster', 'id': 'Cluster'}], None,pd.DataFrame().to_dict()

    @callback(
        Output('download','data'),
        Input('download_button','n_clicks'),
        State('download_df','data'),
        prevent_initial_callback=True
    )
    def download_df(n_clicks,data):
        if not data:
            return None
        
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

        return dict(content=html_content, filename="tabelle.html", type="text/html")

    edition_comparison.run(debug=False, jupyter_mode="external", port=9093)

if __name__ == "__main__":
    pass