#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepseek_python_20260708_1a153f')
    try:
        from django.core.management import execute_from_command_line
    except Exception:
        raise
    execute_from_command_line(sys.argv)
