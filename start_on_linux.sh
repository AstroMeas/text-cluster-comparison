#!/bin/bash

# activate enviroment
source venv/bin/activate

# start app
python scripts/run_app.py "$@"


# `./start.sh --host 0.0.0.0 --port 8080`