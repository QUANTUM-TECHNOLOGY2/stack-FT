import sys
import importlib.util
print('exe:', sys.executable)
print('supabase spec:', importlib.util.find_spec('supabase'))
try:
    import supabase
    print('supabase version:', getattr(supabase, '__version__', 'unknown'))
    from supabase import create_client, Client
    print('create_client:', create_client)
    print('Client:', Client)
except Exception as e:
    print('import error:', repr(e))
