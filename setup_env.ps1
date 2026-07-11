# PowerShell: create venv, install requirements and run server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python deepseek_python_20260708_1a153f.py
