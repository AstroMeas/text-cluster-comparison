# Starts the app on local host
from dash import Dash, html, dcc
import dash

import os
import sys

# Add project path to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import relative modules
from src.web.layouts.main_layout import create_main_layout
from src.web.callbacks import navigation_callbacks, input_callbacks
from src.web.callbacks import analysis_callbacks, download_callbacks, theme_callbacks

# Initialize the app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,  # Important for multi-page apps
    meta_tags=[  # Responsive meta tags
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Set app title
app.title = 'Text Cluster Comparison'

# Define layout
app.layout = create_main_layout()

# Start page URL
app.validation_layout = html.Div([
    create_main_layout(),
])

def run_app(host='127.0.0.1', port=8050, debug=False):
    """Run the Dash app."""
    app.run(debug=debug, host=host, port=port)

if __name__ == '__main__':
    run_app(debug=True)