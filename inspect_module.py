import importlib
import sys
print('sys.path', sys.path[:3])
try:
    m = importlib.import_module('deepseek_python_20260708_1a153f')
    print('module imported', m)
    print('has SETTINGS_DICT', hasattr(m, 'SETTINGS_DICT'))
    if hasattr(m, 'SETTINGS_DICT'):
        print('TEMPLATES in SETTINGS_DICT', m.SETTINGS_DICT.get('TEMPLATES'))
        print('MIDDLEWARE in SETTINGS_DICT', m.SETTINGS_DICT.get('MIDDLEWARE')[:5])
        print('DATABASES in SETTINGS_DICT', m.SETTINGS_DICT.get('DATABASES'))
    print('has TEMPLATE_FILES', hasattr(m, 'TEMPLATE_FILES'))
    print('has TEMPLATES attr', hasattr(m, 'TEMPLATES'))
    if hasattr(m, 'TEMPLATES'):
        print('TEMPLATES attr', m.TEMPLATES)
except Exception as e:
    print('import error', repr(e))
