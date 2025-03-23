@echo off

:: activate enviroment
call venv\Scripts\activate

:: start app
python scripts\run_app.py %*