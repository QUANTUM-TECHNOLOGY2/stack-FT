import deepseek_python_20260708_1a153f as app
from pathlib import Path
from urllib.parse import urlparse

file_url = 'https://whlzpjqmfhshiuupjrjp.supabase.co/storage/v1/object/public/fiches/a6dcab71_ThinkPad_E14_Gen_7_Intel_Spec.pdf'
print('file_url', file_url)
print('parsed file name', Path(urlparse(file_url).path).name)
print('build urls')
for u in app.build_supabase_storage_download_urls(file_url):
    print(' -', u)

path = app.find_local_fallback_path(file_url)
print('fallback path', path)
if path:
    print('exists', path.exists(), 'size', path.stat().st_size)

print('BASE_DIR', app.BASE_DIR)
print('media uploads dirs', list((app.BASE_DIR / 'media' / 'uploads').glob('*')))
