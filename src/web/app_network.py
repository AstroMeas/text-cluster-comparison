# Starts the app in the local network
import os
import sys
import dash
from dash import html, dcc
import socket

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.web.layouts.main_layout import create_main_layout
from src.web.callbacks import register_data_callbacks


def get_local_ip():
    """
    Get the local IP address of the machine.
    This will help to access the app from other devices in the network.
    """
    try:
        # Create a socket connection to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return '127.0.0.1'  # Fallback to localhost if unable to get IP

def create_app(debug=False, dev_tools=False):
    """
    Create and configure the Dash application for network access.
    
    Args:
        debug: Enable debug mode
        dev_tools: Enable dev tools
    
    Returns:
        A configured Dash application
    """
    # Initialize the Dash app
    app = dash.Dash(
        __name__,
        assets_folder='assets',
        suppress_callback_exceptions=True,
        meta_tags=[
            {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}
        ]
    )
    
    # Set up the layout
    app.layout = create_main_layout()
    
    # Import all callbacks
    from src.web.callbacks import register_data_callbacks
    register_data_callbacks(app)
    
    return app

def start_server(host=None, port=8050, debug=False, dev_tools=False):
    """
    Start the Dash server with network configuration.
    
    Args:
        host: Host IP (None for automatic detection)
        port: Port number (default: 8050)
        debug: Enable debug mode
        dev_tools: Enable dev tools
    """
    # Create the app
    app = create_app(debug=debug, dev_tools=dev_tools)
    
    # Use provided host or get local IP
    if host is None:
        host = get_local_ip()
    
    # Print access information
    print(f"Starting server on http://{host}:{port}")
    print(f"You can access the app from other devices using this URL.")
    
    # Run the server - '0.0.0.0' makes it available on the network
    app.run(
        host='0.0.0.0',  # This is crucial to make it accessible on the network
        port=port,
        debug=debug,
        dev_tools_props_check=dev_tools
    )

if __name__ == '__main__':
    start_server(debug=True)