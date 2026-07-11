import requests
import json

url = "https://whlzpjqmfhshiuupjrjp.supabase.co/rest/v1/fiches"
headers = {
    'apikey': 'REPLACE_WITH_SUPABASE_SECRET',
    'Authorization': 'Bearer REPLACE_WITH_SUPABASE_SECRET',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}
payload = {
    'reference': 'FT-TEST-INSERT-001',
    'name': 'Test Insert',
    'author_id': '8651eee5-2d7c-413b-8fb5-7c5231cc684b'
}
try:
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    print('STATUS', r.status_code)
    print(r.text)
except Exception as e:
    print('EXCEPTION', e)
