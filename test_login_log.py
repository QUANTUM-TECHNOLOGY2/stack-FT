import requests
from pathlib import Path
log = Path('test_login_output.txt')
with log.open('w', encoding='utf-8') as f:
    base = 'http://127.0.0.1:8000'
    f.write(f'GET /login {requests.get(base + "/login/").status_code}\n')
    resp = requests.post(base + '/login/', data={'email': 'admin@quantum.local', 'password': 'Test1234!'}, allow_redirects=False)
    f.write(f'POST /login {resp.status_code} {resp.headers.get("Location")}\n')
    f.write(resp.text[:2000] + '\n')
    if resp.status_code in (302, 303):
        url = resp.headers['Location']
        if not url.startswith('http'):
            url = base + url
        r2 = requests.get(url)
        f.write(f'GET dashboard {r2.status_code}\n')
        f.write('dashboard title contains ' + str('Tableau de bord' in r2.text) + '\n')
        f.write('has nav ' + str('<nav' in r2.text) + '\n')
        f.write('has loadFiches ' + str('loadFiches' in r2.text) + '\n')
print('Wrote', log.resolve())
