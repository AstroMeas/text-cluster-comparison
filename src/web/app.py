from dash import Dash

# Import layout
from layouts.main_layout import create_layout

# Import callbacks (they get registered when imported)
from callbacks import data_callbacks, graph_callbacks, download_callbacks

# Initialize the app
app = Dash(__name__)

# Set the app layout
app.layout = create_layout()

# This prevents callback errors on initial load
app.config.suppress_callback_exceptions = True

def run_app(host='127.0.0.1'):
    """Run the Dash app."""
    app.run(debug=False, jupyter_mode="external", port=8050, host=host)

if __name__ == '__main__':
    run_app()