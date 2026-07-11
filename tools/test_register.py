import requests, uuid
url='http://127.0.0.1:8001/api/auth/register/'
email=f'autotest+{uuid.uuid4().hex[:6]}@example.com'
password='TestPass123!'
payload={'email':email,'password':password,'username':'autotest','full_name':'Auto Test'}
print('Testing register with', email)
try:
    r=requests.post(url,json=payload,timeout=10)
    print('Status', r.status_code)
    try:
        print('JSON:', r.json())
    except Exception:
        print('Text:', r.text)
except Exception as e:
    print('Request failed:', e)
