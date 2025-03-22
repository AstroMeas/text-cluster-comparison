from dash import Dash, html, dcc
import dash

# Importiere das Haupt-Layout
from layouts.main_layout import create_main_layout

# Importiere alle Callbacks
from callbacks import navigation_callbacks, input_callbacks
from callbacks import analysis_callbacks, download_callbacks, theme_callbacks

# Initialisiere die App
app = Dash(
    __name__,
    suppress_callback_exceptions=True,  # Wichtig für Multi-Page-Apps
    meta_tags=[  # Responsive Meta-Tags
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Setze den Titel der App
app.title = 'Text Cluster Comparison'

# Definiere das Layout
app.layout = create_main_layout()

# Startseite URL
app.validation_layout = html.Div([
    create_main_layout(),
])

def run_app(host='127.0.0.1', port=8050, debug=False):
    """Run the Dash app."""
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    run_app(debug=True)