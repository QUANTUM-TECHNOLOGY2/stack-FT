import deepseek_python_20260708_1a153f as app
import requests
from pprint import pprint

base = app.SUPABASE_URL.rstrip('/')
headers = {
    'apikey': app.SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {app.SUPABASE_SERVICE_KEY}',
}

endpoints = [
    'storage/v1/bucket',
    'storage/v1/buckets',
    'storage/v1/object/public/fiches',
    'storage/v1/object/fiches',
]
for endpoint in endpoints:
    url = f'{base}/{endpoint}'
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        print('URL:', url)
        print('STATUS:', resp.status_code)
        print('TEXT:', resp.text[:500])
        print('-' * 80)
    except Exception as e:
        print('ERROR', endpoint, str(e))

import pathlib
p = pathlib.Path('media/uploads')
print('LOCAL media/uploads exists:', p.exists())
if p.exists():
    print('LOCAL sample:', list(p.glob('*'))[:20])
