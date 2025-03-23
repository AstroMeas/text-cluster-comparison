# File: src/web/callbacks/__init__.py
from src.web.callbacks import data_callbacks
from src.web.callbacks import graph_callbacks
from src.web.callbacks import input_callbacks
from src.web.callbacks import analysis_callbacks
from src.web.callbacks import navigation_callbacks
from src.web.callbacks import download_callbacks
from src.web.callbacks import theme_callbacks

def register_data_callbacks(app):
    """
    Register all data-related callbacks with the app.
    
    Args:
        app: The Dash application instance
    """
    return app