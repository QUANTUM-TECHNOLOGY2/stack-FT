import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError('Missing SUPABASE_URL or SUPABASE_KEY in environment')

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get all fiches
fiches_response = supabase.table('fiches').select('*').execute()
fiches = fiches_response.data if fiches_response.data else []

print(f'Found {len(fiches)} fiches')

# Fix paths with duplication
for fiche in fiches:
    file_url = fiche.get('file_url', '')
    print(f"ID: {fiche['id']}, Name: {fiche.get('file_name')}, URL: {file_url}")
    
    # Check if path has duplication
    if '/media/uploads/uploads/' in file_url:
        new_url = file_url.replace('/media/uploads/uploads/', '/media/uploads/')
        print(f"  FIXING: {file_url} -> {new_url}")
        
        # Update in database
        supabase.table('fiches').update({'file_url': new_url}).eq('id', fiche['id']).execute()
        print(f"  Updated!")

print("Done!")
