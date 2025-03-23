#!/bin/bash

echo "Install Text-Cluster-Comparison..."

# create virtual enviroment
python3 -m venv venv

# activate enviroment
source venv/bin/activate

# install depencies
pip install -r requirements.txt
pip install -e .

echo "Installation finished! Start application with 'start_on_linux.bat'"