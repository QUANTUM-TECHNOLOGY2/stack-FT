import os
import requests
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY') or os.getenv('SUPABASE_PUBLISHABLE_KEY')
print('SUPABASE_URL=', url)
print('SUPABASE_KEY=', key[:20] + '...' if key else None)
headers = {'apikey': key, 'Content-Type': 'application/json'}
data = {'email': 'yves_test_probe+20260710@example.com', 'password': 'Test1234!'}
try:
    r = requests.post(url.rstrip('/') + '/auth/v1/signup', headers=headers, json=data, timeout=30)
    print('status_code=', r.status_code)
    print('text=', r.text)
except Exception as exc:
    print('exception=', exc)
