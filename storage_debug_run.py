import deepseek_python_20260708_1a153f as app
from pathlib import Path
from urllib.parse import urlparse

resp = app.supabase.table('fiches').select('id,name,file_url,file_name,file_type').limit(20).execute()
print('records:', len(resp.data) if getattr(resp, 'data', None) else 0)
for item in resp.data or []:
    print('---')
    print('id:', item.get('id'))
    print('name:', item.get('name'))
    print('file_name:', item.get('file_name'))
    print('file_type:', item.get('file_type'))
    print('file_url:', item.get('file_url'))
    if item.get('file_url'):
        parsed = urlparse(item.get('file_url'))
        print('path:', parsed.path)
        print('name from url:', Path(parsed.path).name)
        local = Path('media/uploads') / Path(parsed.path).name
        print('local exists:', local.exists(), local)
        if local.exists():
            print('local size:', local.stat().st_size)

local_dir = Path('media/uploads')
print('local dir exists:', local_dir.exists())
if local_dir.exists():
    files = list(local_dir.glob('*'))
    print('local sample count:', len(files))
    for f in files[:20]:
        print('local file:', f.name)
