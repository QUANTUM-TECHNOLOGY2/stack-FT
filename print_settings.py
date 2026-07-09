import importlib
try:
    m = importlib.import_module('deepseek_python_20260708_1a153f')
    s = getattr(m, 'settings', None)
    if s is None:
        print('No settings found on module')
    else:
        print('DEBUG=', getattr(s, 'DEBUG', None))
        print('ALLOWED_HOSTS=', getattr(s, 'ALLOWED_HOSTS', None))
        print('DJANGO_SETTINGS_MODULE=', __import__('os').environ.get('DJANGO_SETTINGS_MODULE'))
except Exception as e:
    import traceback; traceback.print_exc()
