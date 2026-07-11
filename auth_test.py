import requests
import re

session = requests.Session()

print('GET register')
r = session.get('http://localhost:8000/register/')
print(r.status_code)
if r.status_code != 200:
    print(r.text[:800])
    raise SystemExit

m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
print('csrf register', bool(m))
if not m:
    raise SystemExit('csrf token not found')
token = m.group(1)

data = {
    'username': 'testuser',
    'email': 'testuser@example.com',
    'full_name': 'Test User',
    'password1': 'Password123!',
    'password2': 'Password123!',
    'csrfmiddlewaretoken': token,
}

r2 = session.post('http://localhost:8000/register/', data=data, allow_redirects=False)
print('POST register status', r2.status_code)
print('Location', r2.headers.get('Location'))
print(r2.text[:800])

print('GET login')
r3 = session.get('http://localhost:8000/login/')
print(r3.status_code)
m2 = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r3.text)
print('csrf login', bool(m2))
token2 = m2.group(1) if m2 else ''

data2 = {
    'email': 'testuser@example.com',
    'password': 'Password123!',
    'csrfmiddlewaretoken': token2,
}

r4 = session.post('http://localhost:8000/login/', data=data2, allow_redirects=False)
print('POST login status', r4.status_code)
print('Location', r4.headers.get('Location'))
print(r4.text[:800])
