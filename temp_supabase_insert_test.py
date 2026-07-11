import os
from dotenv import load_dotenv
import requests

load_dotenv('.env')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

print('SUPABASE_URL=', SUPABASE_URL)
print('SUPABASE_SERVICE_KEY=', 'set' if SUPABASE_SERVICE_KEY else 'missing')

url = SUPABASE_URL.rstrip('/') + '/rest/v1/fiches'
headers = {
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}
data = {
    'reference': 'TEST-IMPORT',
    'name': 'Test import',
    'description': 'test',
    'category': 'AUTRE',
    'manufacturer': 'Test',
    'version': '1.0',
    'file_url': 'https://example.com',
    'file_name': 'test.pdf',
    'file_size': 123,
    'file_type': 'application/pdf',
    'author_id': '00000000-0000-0000-0000-000000000000'
}

resp = requests.post(url, headers=headers, json=data, timeout=30)
print('status', resp.status_code)
print('text', resp.text)
