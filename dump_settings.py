import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepseek_python_20260708_1a153f')
import django
from django.conf import settings
print('configured', settings.configured)
print('TEMPLATES type', type(settings.TEMPLATES))
print('TEMPLATES len', len(settings.TEMPLATES) if hasattr(settings, 'TEMPLATES') else 'N/A')
print('MIDDLEWARE type', type(settings.MIDDLEWARE))
print('MIDDLEWARE len', len(settings.MIDDLEWARE) if hasattr(settings, 'MIDDLEWARE') else 'N/A')
print('MIDDLEWARE head', settings.MIDDLEWARE[:5] if hasattr(settings, 'MIDDLEWARE') else None)
print('DEBUG', settings.DEBUG)
print('DATABASES', settings.DATABASES.get('default'))
