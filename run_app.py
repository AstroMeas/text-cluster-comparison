import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))


main_dir = os.path.join(current_dir, "text_cluster")
sys.path.insert(0, main_dir)

from text_cluster import dash_app
dash_app.run_app()