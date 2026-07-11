import deepseek_python_20260708_1a153f as app
import requests

resp = app.supabase.table('fiches').select('id,name,file_url,file_name').limit(5).execute()
print('supabase data count:', len(resp.data) if getattr(resp, 'data', None) else 0)
for item in resp.data or []:
    print('id:', item.get('id'), 'file_url:', item.get('file_url'))

ids = [item['id'] for item in (resp.data or []) if item.get('file_url')]
print('download ids:', ids)
if ids:
    url = f'http://127.0.0.1:8000/api/fiches/{ids[0]}/download/'
    print('download url:', url)
    try:
        r = requests.get(url, allow_redirects=False, timeout=30)
        print('status', r.status_code)
        print('headers', {k:v for k,v in r.headers.items() if k.lower() in ['content-type','content-disposition','content-length']})
        if r.status_code != 200:
            print('body', r.text[:500])
        else:
            print('body', 'OK')
    except Exception as e:
        print('error', e)
