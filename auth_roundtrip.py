import requests
import re
import random
import string

email = 'user' + ''.join(random.choices(string.digits, k=6)) + '@example.com'
password = 'Password123!'
print('Testing with', email)

s = requests.Session()
r = s.get('http://localhost:8000/register/')
if r.status_code != 200:
    print('GET register failed', r.status_code)
    print(r.text[:400])
    raise SystemExit
m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
if not m:
    print('csrf token missing')
    raise SystemExit
csrf = m.group(1)

r = s.post('http://localhost:8000/register/', data={
    'username': 'testuser',
    'email': email,
    'full_name': 'Test User',
    'password1': password,
    'password2': password,
    'csrfmiddlewaretoken': csrf,
}, allow_redirects=False)
print('register status', r.status_code)
print('register location', r.headers.get('Location'))
print('register body contains error', 'Erreur' in r.text or 'error' in r.text)
print('register body snippet', r.text[:400])

r = s.get('http://localhost:8000/login/')
if r.status_code != 200:
    print('GET login failed', r.status_code)
    raise SystemExit
m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
if not m:
    print('csrf login missing')
    raise SystemExit
csrf = m.group(1)

r = s.post('http://localhost:8000/login/', data={
    'email': email,
    'password': password,
    'csrfmiddlewaretoken': csrf,
}, allow_redirects=False)
print('login status', r.status_code)
print('login location', r.headers.get('Location'))
print('login body snippet', r.text[:400])
