import pandas as pd
from dash import dcc

def download_df(n_clicks, data, format, filename):
    """
    Prepares data for download in specified format.
    
    Args:
        n_clicks: Number of button clicks
        data: Data to download
        format: Download format (html or csv)
        filename: Base filename without extension
        
    Returns:
        dict or None: Download data dictionary or None if no data to download
    """
    if not data:
        return None
    
    if format == 'html':
        df = pd.DataFrame(data)
        
        # CSS styling for HTML table
        style = """
        <style>
            table { width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; }
            th { background-color: lightgrey; font-weight: bold; text-align: left; padding: 8px; }
            td { min-width: 20px; max-width: 400px; word-wrap: break-word; padding: 8px; border: 1px solid #ddd; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:hover { background-color: #ddd; }
        </style>
        """

        # Pandas Styler for HTML table
        html_table = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', 'lightgrey'), ('font-weight', 'bold'), ('text-align', 'left')]},
            {'selector': 'td', 'props': [('text-align', 'left'), ('min-width', '20px'), ('max-width', '400px'), ('word-wrap', 'break-word')]},
            {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
            {'selector': 'tr:hover', 'props': [('background-color', '#ddd')]}
        ]).to_html()

        # HTML content with styling
        html_content = f"{style}\n{html_table}"

        return dict(content=html_content, filename=f"{filename}.html", type="text/html")
    
    elif format == 'csv':
        df = pd.DataFrame(data)
        return dcc.send_data_frame(df.to_csv, f"{filename}.csv", index=False)
    
    else:
        return None