import deepseek_python_20260708_1a153f as app
import requests
from pprint import pprint
base = app.SUPABASE_URL.rstrip('/')
print('SUPABASE_URL', base)
headers = {'apikey': app.SUPABASE_SERVICE_KEY, 'Authorization': f'Bearer {app.SUPABASE_SERVICE_KEY}'}
for path in ['storage/v1/bucket', 'storage/v1/object/public/fiches/a6dcab71_ThinkPad_E14_Gen_7_Intel_Spec.pdf', 'storage/v1/object/fiches/a6dcab71_ThinkPad_E14_Gen_7_Intel_Spec.pdf']:
    url = f'{base}/{path}'
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print('\nURL=', url)
        print('status=', r.status_code)
        print('headers=', {k:v for k,v in r.headers.items() if k.lower() in ['content-type','content-length','sb-request-id']})
        print('body=', r.text[:400])
    except Exception as exc:
        print('URL=', url, 'exc=', exc)
