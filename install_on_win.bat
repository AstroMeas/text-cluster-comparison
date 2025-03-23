@echo off
echo Install Text-Cluster-Comparison...

:: create virtual envorement
python -m venv venv

:: activate enviroment
call venv\Scripts\activate

:: install dependencies
pip install -r requirements.txt
pip install -e .

echo Installation finished! Start application with 'start_on_win.bat'