import sqlite3
from pathlib import Path

db_path = Path('data/app.sqlite3')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check fiches
print('=== FICHES TABLE ===')
cursor.execute('SELECT COUNT(*) as count FROM fiches')
result = cursor.fetchone()
print(f'Total fiches: {result["count"]}')

print('\n=== FICHES DATA ===')
cursor.execute('SELECT id, reference, name, category, file_url FROM fiches LIMIT 10')
for row in cursor.fetchall():
    print(f'ID: {row["id"]}')
    print(f'  Reference: {row["reference"]}')
    print(f'  Name: {row["name"]}')
    print(f'  Category: {row["category"]}')
    print(f'  File URL: {row["file_url"][:50] if row["file_url"] else "None"}...')
    print()

# Check tags
print('=== TAGS TABLE ===')
cursor.execute('SELECT COUNT(*) as count FROM tags')
result = cursor.fetchone()
print(f'Total tags: {result["count"]}')

cursor.execute('SELECT id, name FROM tags')
for row in cursor.fetchall():
    print(f'  - {row["name"]}')

# Check fiche_tags
print('\n=== FICHE_TAGS TABLE ===')
cursor.execute('SELECT COUNT(*) as count FROM fiche_tags')
result = cursor.fetchone()
print(f'Total fiche_tags: {result["count"]}')

conn.close()
