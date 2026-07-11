import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path.cwd() / '.env')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

print('SUPABASE_URL', SUPABASE_URL)
print('SUPABASE_KEY', SUPABASE_KEY[:10] + '...' if SUPABASE_KEY else None)

url = f"{SUPABASE_URL}/auth/v1/signup"
headers = {'apikey': SUPABASE_KEY, 'Content-Type': 'application/json'}
data = {'email': 'probeuser@example.com', 'password': 'Password123!'}
resp = requests.post(url, headers=headers, json=data, timeout=30)
print('status', resp.status_code)
print('headers', resp.headers)
print('text', resp.text)

url2 = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
resp2 = requests.post(url2, headers=headers, json=data, timeout=30)
print('login status', resp2.status_code)
print('login text', resp2.text)
