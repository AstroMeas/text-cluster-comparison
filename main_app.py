# File: scripts/run_app.py
import argparse

# Add project root to path
from src.web.app_network import start_server

def main():
    """
    Main function to run the Dash app with command line arguments.
    """
    parser = argparse.ArgumentParser(description='Run the text-cluster-comparison app on the network')
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8050, 
        help='Port to run the app on (default: 8050)'
    )
    
    parser.add_argument(
        '--host', 
        type=str, 
        default=None, 
        help='Host IP address (default: auto-detect)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true', 
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Start the server with the provided arguments
    start_server(
        host=args.host,
        port=args.port,
        debug=args.debug
    )

if __name__ == '__main__':
    main()