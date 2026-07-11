import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepseek_python_20260708_1a153f')
import django
from django.conf import settings
print('configured', settings.configured)
print('TEMPLATES', settings.TEMPLATES)
print('MIDDLEWARE', settings.MIDDLEWARE)
print('DATABASES', settings.DATABASES)
print('DEBUG', settings.DEBUG)
