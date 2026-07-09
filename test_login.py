import requests

base = 'http://127.0.0.1:8000'
print('GET /login', requests.get(base + '/login/').status_code)
resp = requests.post(base + '/login/', data={'email': 'admin@quantum.local', 'password': 'Test1234!'}, allow_redirects=False)
print('POST /login', resp.status_code, resp.headers.get('Location'))
print(resp.text[:800])
if resp.status_code in (302, 303):
    url = resp.headers['Location']
    if not url.startswith('http'):
        url = base + url
    r2 = requests.get(url)
    print('GET dashboard', r2.status_code)
    print('dashboard title contains', 'Tableau de bord' in r2.text)
    print('has nav', '<nav' in r2.text)
    print('has loadFiches', 'loadFiches' in r2.text)
