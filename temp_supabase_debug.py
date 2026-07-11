import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY') or os.getenv('SUPABASE_PUBLISHABLE_KEY')
service = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SECRET_KEY')
print('URL=', url)
print('KEY=', key[:20] + '...' if key else None)
print('SERVICE=', service[:20] + '...' if service else None)
for email in ['yves@gmail.com', 'browseruser826130@example.com', 'testuser_bis_20260710@example.com']:
    print('\n--- SIGNUP', email)
    try:
        r = requests.post(url.rstrip('/') + '/auth/v1/signup', headers={'apikey': key, 'Content-Type': 'application/json'}, json={'email': email, 'password': 'Test1234!'}, timeout=30)
        print('status', r.status_code)
        print('text', r.text)
    except Exception as e:
        print('signup exception', e)
    if service:
        print('--- ADMIN', email)
        try:
            r = requests.post(url.rstrip('/') + '/auth/v1/admin/users', headers={'apikey': service, 'Authorization': f'Bearer {service}', 'Content-Type': 'application/json'}, json={'email': email, 'password': 'Test1234!', 'email_confirm': True}, timeout=30)
            print('status', r.status_code)
            print('text', r.text)
        except Exception as e:
            print('admin exception', e)
