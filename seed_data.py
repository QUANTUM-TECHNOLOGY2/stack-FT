import os
import uuid
import json
from pathlib import Path
from local_backend import create_local_backend

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
backend = create_local_backend(BASE_DIR, MEDIA_ROOT)

print('Using local backend DB:', backend.db_path)

# Create default user
email = 'admin@quantum.local'
password = 'Test1234!'
existing = backend._conn().execute('SELECT id FROM auth_users WHERE email = ?', (email,)).fetchone()
if existing:
    user_id = existing['id']
    print('User already exists:', email)
else:
    result = backend.auth.sign_up({'email': email, 'password': password})
    user_id = result.user.id
    print('Created user:', email)

# Create profile
conn = backend._conn()
profile = conn.execute('SELECT id FROM profiles WHERE id = ?', (user_id,)).fetchone()
if not profile:
    conn.execute('INSERT INTO profiles (id, username, full_name, role) VALUES (?, ?, ?, ?)',
                 (user_id, 'admin', 'Quantum Admin', 'admin'))
    conn.commit()
    print('Created profile for', email)
else:
    print('Profile already exists for', email)
conn.close()

# Create sample tags
tag_ids = {}
tag_names = ['qualité', 'sécurité', 'électronique', 'procédé']
for name in tag_names:
    existing = backend._conn().execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()
    if existing:
        tag_ids[name] = existing['id']
    else:
        tag_id = str(uuid.uuid4())
        backend._conn().execute('INSERT INTO tags (id, name, color) VALUES (?, ?, ?)', (tag_id, name, '#293462'))
        backend._conn().commit()
        tag_ids[name] = tag_id

# Create sample fiche records
samples = [
    {
        'reference': 'FT-2026-0001',
        'name': 'Boîtier électronique haute fiabilité',
        'description': 'Fiche technique pour le boîtier électronique utilisé en environnement industriel.',
        'category': 'ELECTRONIQUE',
        'manufacturer': 'Quantum Systems',
        'version': '1.0',
        'file_name': 'boitier.txt',
        'file_type': 'text/plain',
        'tags': ['qualité', 'sécurité', 'électronique']
    },
    {
        'reference': 'FT-2026-0002',
        'name': 'Procédé d’assemblage mécanique',
        'description': 'Processus qualité pour l’assemblage des modules mécaniques.',
        'category': 'MECANIQUE',
        'manufacturer': 'Quantum Systems',
        'version': '1.0',
        'file_name': 'procedure.txt',
        'file_type': 'text/plain',
        'tags': ['qualité', 'procédé']
    },
]

for sample in samples:
    existing = backend._conn().execute('SELECT id FROM fiches WHERE reference = ?', (sample['reference'],)).fetchone()
    if existing:
        print('Sample fiche exists:', sample['reference'])
        continue
    file_data = f"{sample['name']}\n{sample['description']}\n".encode('utf-8')
    upload_result = backend.storage.from_('fiches').upload(sample['file_name'], file_data)
    if not upload_result:
        print('Failed to upload sample file', sample['file_name'])
        continue
    fiche_id = str(uuid.uuid4())
    with backend._conn() as conn:
        conn.execute(
            'INSERT INTO fiches (id, reference, name, description, category, manufacturer, version, file_url, file_name, file_size, file_type, file_preview, author_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                fiche_id,
                sample['reference'],
                sample['name'],
                sample['description'],
                sample['category'],
                sample['manufacturer'],
                sample['version'],
                upload_result if isinstance(upload_result, str) else upload_result,
                sample['file_name'],
                len(file_data),
                sample['file_type'],
                json.dumps({'type': sample['file_type'], 'text': sample['description']}),
                user_id,
            )
        )
        conn.commit()
    for tag_name in sample['tags']:
        tag_id = tag_ids.get(tag_name)
        if tag_id:
            with backend._conn() as conn:
                conn.execute('INSERT OR IGNORE INTO fiche_tags (fiche_id, tag_id) VALUES (?, ?)', (fiche_id, tag_id))
                conn.commit()
    print('Created sample fiche:', sample['reference'])

print('Ready. Login with:', email, '/', password)
