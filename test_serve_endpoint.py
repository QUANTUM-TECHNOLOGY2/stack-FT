import requests

url = 'http://localhost:8000/api/fiches/ee6ad1d2-b166-4797-a331-d137c2b9ce01/serve/'
print('Requesting', url)
try:
    r = requests.get(url, timeout=10)
    print('status', r.status_code)
    print('headers')
    for k, v in r.headers.items():
        print(k, ':', v)
    print('text_preview', r.text[:500])
except Exception as e:
    print('EXCEPTION', type(e).__name__, e)
