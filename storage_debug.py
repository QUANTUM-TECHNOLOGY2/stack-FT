import deepseek_python_20260708_1a153f as app
from pprint import pprint
from urllib.parse import urlparse

print('SUPABASE_URL', app.SUPABASE_URL)
print('SUPABASE_KEY set', bool(app.SUPABASE_KEY))
print('SUPABASE_SERVICE_KEY set', bool(app.SUPABASE_SERVICE_KEY))

try:
    resp = app.supabase.table('fiches').select('id,name,file_url,file_name,file_type').limit(10).execute()
    print('status', getattr(resp, 'status_code', None))
    print('data count', len(resp.data) if getattr(resp, 'data', None) else 0)
    print('data:')
    pprint(resp.data)
    if resp.data:
        for item in resp.data:
            url = item.get('file_url')
            print('---')
            print('orig', url)
            if url:
                print('parsed scheme/netloc/path:', (urlparse(url).scheme, urlparse(url).netloc, urlparse(url).path))
                print('extracted path:', app.extract_storage_path(url))
                print('download url:', app.build_supabase_storage_download_url(url))
except Exception as e:
    import traceback
    traceback.print_exc()
