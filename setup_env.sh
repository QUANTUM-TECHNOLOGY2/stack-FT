#!/usr/bin/env bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python deepseek_python_20260708_1a153f.py
