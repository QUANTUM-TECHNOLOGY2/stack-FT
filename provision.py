import importlib, sys, time
print('starting provision')
try:
    m = importlib.import_module('deepseek_python_20260708_1a153f')
    print('imported app')
    from django.core.management import call_command
    print('running migrate...')
    call_command('migrate','--noinput')
    print('migrate done')
except Exception as e:
    print('migrate error', e)

# create supabase test user via REST
import requests
SUPA='https://your-supabase-url.supabase.co'
ANON='[YOUR_ANON_KEY]'
SERVICE='[YOUR_SERVICE_KEY]'
email='testuser@example.com'
password='Testpass123'
try:
    print('signup request...')
    r = requests.post(SUPA + '/auth/v1/signup', json={'email': email, 'password': password}, headers={'apikey': ANON, 'Content-Type': 'application/json'}, timeout=20)
    print('signup status', r.status_code)
    print(r.text)
    resp = r.json()
    if 'user' in resp and resp['user'] and resp['user'].get('id'):
        uid = resp['user']['id']
        print('create profile for', uid)
        profile = {'id': uid, 'username': 'testuser', 'full_name': 'Test User', 'role':'user'}
        r2 = requests.post(SUPA + '/rest/v1/profiles', json=profile, headers={'apikey': SERVICE, 'Authorization': f'Bearer {SERVICE}', 'Content-Type': 'application/json', 'Prefer':'return=representation'}, timeout=20)
        print('profile status', r2.status_code)
        print(r2.text)
except Exception as e:
    print('signup error', e)

# try login via API
try:
    print('login attempt...')
    r3 = requests.post('http://localhost:8000/api/auth/login/', json={'email': email, 'password': password}, timeout=15)
    print('local login status', r3.status_code)
    print(r3.text)
except Exception as e:
    print('local login error', e)

print('provision finished')
