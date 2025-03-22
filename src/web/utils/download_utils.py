import pandas as pd
from dash import dcc

def prepare_download(data, format, filename):
    """
    Prepares data for download in specified format.
    
    Args:
        data (dict): Data to be downloaded
        format (str): Download format ('csv' or 'html')
        filename (str): Base filename without extension
        
    Returns:
        dict: Download data dictionary for dcc.Download component
    """
    if not data:
        return None
    
    # Convert to DataFrame if it's a dict
    df = pd.DataFrame(data)
    
    if format == 'html':
        # Create HTML table with styling
        style = """
        <style>
            table { 
                width: 100%; 
                border-collapse: collapse; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                margin-bottom: 20px;
            }
            th { 
                background-color: #f8f9fa; 
                color: #212529;
                font-weight: bold; 
                text-align: left; 
                padding: 12px 8px; 
                border: 1px solid #dee2e6;
            }
            td { 
                padding: 12px 8px; 
                border: 1px solid #dee2e6; 
                word-wrap: break-word;
                vertical-align: top;
            }
            tr:nth-child(even) { 
                background-color: #f8f9fa; 
            }
            tr:hover { 
                background-color: #e9ecef; 
            }
            h1 {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                color: #212529;
            }
            .timestamp {
                font-size: 0.8em;
                color: #6c757d;
                margin-bottom: 20px;
            }
        </style>
        """
        
        # Add timestamp and title
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"""
        <h1>{filename.replace('_', ' ').title()}</h1>
        <div class="timestamp">Generated: {timestamp}</div>
        """
        
        # Generate HTML table
        html_table = df.to_html(
            index=False,
            border=0,
            classes='data-table',
            na_rep='',
            float_format=lambda x: f"{x:.2f}" if isinstance(x, float) else x
        )
        
        # Combine all parts
        html_content = f"{style}\n{header}\n{html_table}"
        
        return dict(
            content=html_content,
            filename=f"{filename}.html",
            type="text/html"
        )
    
    elif format == 'csv':
        return dcc.send_data_frame(
            df.to_csv,
            f"{filename}.csv",
            index=False
        )
    
    else:
        return None