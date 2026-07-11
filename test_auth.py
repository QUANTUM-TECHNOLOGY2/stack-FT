#!/usr/bin/env python
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

print('🧪 Test d\'inscription Supabase Auth...')

headers = {
    'apikey': SUPABASE_KEY,
    'Content-Type': 'application/json'
}

data = {
    'email': 'testuser@test.com',
    'password': 'TestPass123'
}

try:
    resp = requests.post(f'{SUPABASE_URL}/auth/v1/signup', headers=headers, json=data, timeout=5)
    print(f'Status: {resp.status_code}')
    print(f'Response: {resp.text}')
    
    if resp.status_code < 400:
        user_data = resp.json()
        print(f'✅ User créé: {user_data.get("user", {}).get("id")}')
    else:
        print(f'❌ Erreur: {resp.text}')
except Exception as e:
    print(f'❌ Erreur: {e}')
