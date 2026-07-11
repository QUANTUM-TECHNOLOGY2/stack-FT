import requests
import re

session = requests.Session()

r = session.get('http://localhost:8000/register/')
print('GET register', r.status_code)
print('cookies after GET register:', session.cookies.get_dict())

m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
print('csrf register found:', bool(m))
token = m.group(1) if m else ''
print('csrf token:', token[:20])

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
print('register headers:', {k:v for k,v in r2.headers.items() if k.lower() in ('location','set-cookie')})
print('register cookies after POST:', session.cookies.get_dict())
print('register body contains error:', 'Erreur' in r2.text or 'error' in r2.text)
print('register body snippet:', r2.text[r2.text.find('<body'):r2.text.find('</body>')+7] if '<body' in r2.text else r2.text[:400])

r3 = session.get('http://localhost:8000/login/')
print('GET login', r3.status_code)
print('cookies after GET login:', session.cookies.get_dict())

m2 = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r3.text)
print('csrf login found:', bool(m2))
token2 = m2.group(1) if m2 else ''
print('csrf login token:', token2[:20])

data2 = {
    'email': 'testuser@example.com',
    'password': 'Password123!',
    'csrfmiddlewaretoken': token2,
}

r4 = session.post('http://localhost:8000/login/', data=data2, allow_redirects=False)
print('POST login status', r4.status_code)
print('login headers:', {k:v for k,v in r4.headers.items() if k.lower() in ('location','set-cookie')})
print('login cookies after POST:', session.cookies.get_dict())
print('login body contains error:', 'Identifiants invalides' in r4.text or 'Erreur' in r4.text)
print('login body snippet:', r4.text[r4.text.find('<body'):r4.text.find('</body>')+7] if '<body' in r4.text else r4.text[:400])
