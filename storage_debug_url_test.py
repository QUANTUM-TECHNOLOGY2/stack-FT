import deepseek_python_20260708_1a153f as app
import requests

file_url = 'https://whlzpjqmfhshiuupjrjp.supabase.co/storage/v1/object/public/fiches/a6dcab71_ThinkPad_E14_Gen_7_Intel_Spec.pdf'
alt_url = app.build_supabase_storage_download_url(file_url)
print('file_url=', file_url)
print('alt_url=', alt_url)

headers = {
    'apikey': app.SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {app.SUPABASE_SERVICE_KEY}',
}

for name, url in [('public', file_url), ('alternate', alt_url)]:
    print('---', name)
    try:
        r = requests.get(url, timeout=30)
        print('no auth status', r.status_code)
        print('no auth headers', {k:v for k,v in r.headers.items() if k.lower() in ['content-type','content-length','sb-request-id']})
        print('no auth text head', r.text[:200])
    except Exception as e:
        print('no auth error', e)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print('auth status', r.status_code)
        print('auth headers', {k:v for k,v in r.headers.items() if k.lower() in ['content-type','content-length','sb-request-id']})
        print('auth text head', r.text[:200])
    except Exception as e:
        print('auth error', e)
