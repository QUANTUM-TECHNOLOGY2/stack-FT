import json
from pathlib import Path
import deepseek_python_20260708_1a153f as app

print('supabase', getattr(app.supabase, 'url', None), getattr(app.supabase, 'key', None) is not None)
resp = app.supabase.table('fiches').select('id,reference,name').limit(3).execute()
print('raw status', getattr(resp, 'status_code', None), 'rows', len(resp.data) if resp.data else 0)
print(json.dumps(resp.data[:5], indent=2, ensure_ascii=False))
search = 'Test'
resp2 = app.supabase.table('fiches').select('id,reference,name').or_(f"reference.ilike.%{search}%,name.ilike.%{search}%").execute()
print('search status', getattr(resp2, 'status_code', None), 'rows', len(resp2.data) if resp2.data else 0)
print(json.dumps(resp2.data[:5], indent=2, ensure_ascii=False))
