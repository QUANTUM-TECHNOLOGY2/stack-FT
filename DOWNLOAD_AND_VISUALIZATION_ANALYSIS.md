# Django Download & PDF Visualization Analysis
## Quantum Technology App - deepseek_python_20260708_1a153f.py

---

## 1. DOWNLOAD ENDPOINT LOGIC

### Endpoint: `/api/fiches/<fiche_id>/download/` (api_fiche_download)
**Location**: Lines 1277-1300

```python
@login_required_api
def api_fiche_download(request, fiche_id):
    try:
        response = supabase.table('fiches').select('file_url, file_name').eq('id', fiche_id).execute()
        if not response.data or not response.data[0].get('file_url'):
            return JsonResponse({'error': 'Fichier non trouvé'}, status=404)
        
        fiche = response.data[0]
        file_url = fiche['file_url']
        file_name = fiche.get('file_name', 'document')
        
        # LOCAL FILE SERVING
        if file_url.startswith('/media/'):
            local_path = BASE_DIR / file_url.lstrip('/')
            if not local_path.exists():
                return JsonResponse({'error': 'Fichier non trouvé'}, status=404)
            response = FileResponse(local_path.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
        
        # REMOTE FILE SERVING (Supabase)
        file_response = requests.get(file_url)
        if file_response.status_code != 200:
            return JsonResponse({'error': 'Erreur de téléchargement'}, status=500)
        
        response = HttpResponse(file_response.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

**File Paths Used**:
- **Local**: `/media/uploads/` (resolves from `BASE_DIR / file_url.lstrip('/')`)
- **Remote**: Supabase Storage URLs (e.g., `https://...supabase.co/storage/v1/object/public/fiches/...`)

**Flow**:
1. Fetch fiche record from Supabase DB
2. Check if `file_url` starts with `/media/`
   - YES → Serve from local filesystem using `FileResponse`
   - NO → Download from Supabase and proxy through HTTP response

---

### Endpoint: `/api/fiches/<fiche_id>/versions/<version_id>/download/` (api_version_download)
**Location**: Lines 1302-1326

```python
@login_required_api
def api_version_download(request, fiche_id, version_id):
    try:
        response = supabase.table('versions').select('file_url, file_name').eq('id', version_id).eq('fiche_id', fiche_id).execute()
        if not response.data or not response.data[0].get('file_url'):
            return JsonResponse({'error': 'Version non trouvée'}, status=404)
        
        version = response.data[0]
        file_url = version.get('file_url', '')
        
        # LOCAL FILE SERVING
        if file_url.startswith('/media/'):
            local_path = BASE_DIR / file_url.lstrip('/')
            if not local_path.exists():
                return JsonResponse({'error': 'Version non trouvée'}, status=404)
            response = FileResponse(local_path.open('rb'))
            response['Content-Disposition'] = f'attachment; filename="{version.get("file_name", "version")}"'
            return response
        
        # REMOTE FILE SERVING
        file_response = requests.get(file_url)
        if file_response.status_code != 200:
            return JsonResponse({'error': 'Erreur de téléchargement'}, status=500)
        
        response = HttpResponse(file_response.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{version.get("file_name", "version")}"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

**Identical logic to main download but queries `versions` table instead of `fiches` table.**

---

## 2. PDF VIEWING/VISUALIZATION ENDPOINT LOGIC

### Endpoint: `/api/fiches/<fiche_id>/view/` (api_fiche_view)
**Location**: Lines 1328-1352

```python
@login_required_api
def api_fiche_view(request, fiche_id):
    try:
        response = supabase.table('fiches').select('id, name, reference, file_url, file_type, file_preview').eq('id', fiche_id).execute()
        if not response.data:
            return JsonResponse({'error': 'Fiche non trouvée'}, status=404)
        
        fiche = response.data[0]
        preview = fiche.get('file_preview', {})
        if isinstance(preview, str):
            try:
                preview = json.loads(preview)
            except:
                preview = {}
        
        return JsonResponse({
            'id': fiche['id'],
            'name': fiche['name'],
            'reference': fiche['reference'],
            'file_type': fiche.get('file_type', ''),
            'file_url': fiche.get('file_url', ''),
            'preview': preview,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

**Returns**:
- `file_url`: Direct URL to file (can be local `/media/...` or Supabase URL)
- `file_type`: MIME type (e.g., `application/pdf`)
- `preview`: Pre-generated metadata (pages, text excerpt, images)

---

## 3. HOW FILE URLS ARE GENERATED FOR FRONTEND

### Upload & URL Generation: `supabase_upload_file()`
**Location**: Lines 623-656

```python
def supabase_upload_file(file_data, filename):
    """Upload un fichier vers Supabase Storage"""
    try:
        # Générer un nom unique
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        file_path = f"uploads/{unique_name}"
        content_type = guess_mime_from_extension(filename) or 'application/octet-stream'

        # Upload vers Supabase Storage
        response = supabase.storage.from_('fiches').upload(
            file_path,
            file_data,
            {'content-type': content_type}
        )

        if response:
            public_result = supabase.storage.from_('fiches').get_public_url(file_path)
            public_url = None
            if isinstance(public_result, dict):
                public_url = public_result.get('public_url') or public_result.get('publicUrl')
                if not public_url:
                    data = public_result.get('data')
                    if isinstance(data, dict):
                        public_url = data.get('public_url') or data.get('publicUrl')
            elif hasattr(public_result, 'data') and isinstance(public_result.data, dict):
                public_url = public_result.data.get('public_url') or public_result.data.get('publicUrl')
            elif isinstance(public_result, str):
                public_url = public_result
            if not public_url:
                public_url = str(public_result)

            return {
                'success': True,
                'url': public_url,
                'path': file_path,
                'name': filename
            }
        return {'success': False, 'error': 'Upload failed'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

**URL Generation Flow**:
1. **Local Backend**: URLs stored as `/media/uploads/{uuid}_{filename}`
2. **Supabase Storage**: URLs follow pattern `{SUPABASE_URL}/storage/v1/object/public/fiches/uploads/{uuid}_{filename}`

### Where URLs are used in Frontend (dashboard.html):
**Line ~2315-2335** (in JavaScript):

```javascript
async function viewFiche(id) {
    // ... fetch /api/fiches/{id}/view/
    const data = await response.json();
    
    let html = '';
    if (data.file_type && data.file_type.includes('pdf')) {
        // ✅ PDF EMBEDDING
        html = `<iframe class="pdf-viewer" src="${data.file_url}#toolbar=0"></iframe>`;
    } else if (data.file_type && data.file_type.includes('image')) {
        // ✅ IMAGE EMBEDDING
        html = `<img class="image-viewer" src="${data.file_url}" alt="${data.name}"></div>`;
    } else if (preview.text) {
        // ✅ TEXT PREVIEW
        html = `<div class="text-viewer">${escapeHtml(preview.text)}</div>`;
    }
}
```

---

## 4. MIDDLEWARE & STATIC FILE SERVING CONFIGURATION

### Django Settings (SETTINGS_DICT):
**Location**: Lines 340-439

```python
'MIDDLEWARE': [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
],

'STATIC_URL': '/static/',
'STATIC_ROOT': STATIC_ROOT,  # BASE_DIR / 'staticfiles'
'STATICFILES_DIRS': [BASE_DIR / 'static'],
'MEDIA_ROOT': MEDIA_ROOT,    # BASE_DIR / 'media'
'MEDIA_URL': MEDIA_URL,      # '/media/'
```

### URL Configuration:
**Location**: Lines 2641-2665

```python
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**This means**:
- In DEBUG mode, Django serves `/static/` and `/media/` directly
- `/media/uploads/` maps to `c:\Users\kpeho\Downloads\Quantum\media\uploads\`
- Local files stored with paths like `/media/uploads/{uuid}_{filename}.pdf`

---

### Directory Creation (auto-creation on startup):
**Location**: Lines 519-521

```python
os.makedirs(BASE_DIR / 'templates', exist_ok=True)
os.makedirs(BASE_DIR / 'static', exist_ok=True)
os.makedirs(MEDIA_ROOT / 'uploads', exist_ok=True)  # Creates /media/uploads/
```

---

## 5. FILE STORAGE VERIFICATION

### Current State of `/media/uploads/`:
✅ **Directory EXISTS and contains files**:
```
15daa714_ThinkPad_E14_Gen_7_Intel_Spec.pdf
4d2c6dc8_ThinkPad_E14_Gen_7_Intel_Spec.pdf
6f1bbe87_ThinkPad_E14_Gen_7_Intel_Spec.pdf
fe7db809_ThinkPad_E14_Gen_7_Intel_Spec.pdf
```

**File Naming Pattern**: `{8-char-uuid}_{original_filename}`

### Upload Logic (api_fiche_create):
**Location**: Lines 1050-1100

```python
# Upload do fichier vers Supabase Storage
file_data = file.read()
if len(file_data) > MAX_FILE_SIZE:
    return JsonResponse({'error': 'Le fichier doit faire 50 MB maximum'}, status=400)
upload_result = supabase_upload_file(file_data, file.name)

# Then stored in DB:
fiche_data = {
    'file_url': upload_result['url'],  # ← THIS IS KEY
    'file_name': upload_result['name'],
    'file_size': len(file_data),
    'file_type': file_type,
    'file_preview': json.dumps(preview),
}
```

---

## ⚠️ ISSUES FOUND IN DOWNLOAD & VISUALIZATION

### **ISSUE #1: Path Resolution Bug in Local File Serving**
**Severity**: 🔴 CRITICAL
**Location**: Lines 1288-1289 (download) & 1314-1315 (version download)

```python
if file_url.startswith('/media/'):
    local_path = BASE_DIR / file_url.lstrip('/')  # ← PROBLEM HERE
```

**Problem**:
- `file_url` = `/media/uploads/15daa714_file.pdf`
- After `lstrip('/')` = `media/uploads/15daa714_file.pdf`
- `BASE_DIR / 'media/uploads/...'` = `c:\Users\kpeho\Downloads\Quantum\media\uploads\...`
- ✅ This WORKS correctly!

**However**, if `file_url` is stored as a full Supabase URL instead of `/media/...`, it won't serve correctly.

---

### **ISSUE #2: Frontend PDF Viewer Uses iframe with Direct URL**
**Severity**: 🟡 MEDIUM
**Location**: Lines 2333-2334 (dashboard.html JavaScript)

```javascript
html = `<iframe class="pdf-viewer" src="${data.file_url}#toolbar=0"></iframe>`;
```

**Problem**:
- If `file_url` is a local path like `/media/uploads/...`, the iframe SRC should work ✅
- But if it's a Supabase URL, it may require CORS headers
- **Supabase Storage may block direct iframe embedding** without proper CORS setup

**Alternative**: Use PDF.js library or proxy through Django endpoint

---

### **ISSUE #3: Content-Disposition Filename Encoding**
**Severity**: 🟡 MEDIUM
**Location**: Lines 1295, 1296, 1322, 1323

```python
response['Content-Disposition'] = f'attachment; filename="{file_name}"'
```

**Problem**:
- If `file_name` contains special characters or non-ASCII (e.g., "Fiche_Technique_français.pdf")
- Header should use RFC 5987 encoding: `filename*=UTF-8''...`
- Current code will break on non-ASCII filenames

**Fix**: Use proper encoding
```python
from django.utils.http import urlquote
response['Content-Disposition'] = f'attachment; filename="{urlquote(file_name)}"'
```

---

### **ISSUE #4: Preview Generation Only Done at Upload**
**Severity**: 🟡 MEDIUM  
**Location**: Lines 1096-1098 (api_fiche_create)

```python
preview = generate_file_preview(file_data, file_type)
if preview:
    fiche_data['file_preview'] = json.dumps(preview)
```

**Problem**:
- Preview is generated ONLY when file is first uploaded
- If file is replaced via version update, old preview is used
- Version records DON'T have `file_preview` field

**Current**: PDF pages counted from main fiche preview only ✅
**But**: Version history doesn't show page counts

---

### **ISSUE #5: No File Type Validation for Download**
**Severity**: 🟡 MEDIUM
**Location**: Lines 1302-1326 (api_version_download & api_fiche_download)

```python
response = HttpResponse(file_response.content, content_type='application/octet-stream')
```

**Problem**:
- Always returns `application/octet-stream` regardless of actual file type
- Should use the stored `file_type` from DB
- Example:
  ```python
  content_type = fiche.get('file_type', 'application/octet-stream')
  response = HttpResponse(file_response.content, content_type=content_type)
  ```

---

### **ISSUE #6: No Error Handling for Corrupted Local Files**
**Severity**: 🟡 MEDIUM
**Location**: Lines 1290-1292

```python
if not local_path.exists():
    return JsonResponse({'error': 'Fichier non trouvé'}, status=404)
response = FileResponse(local_path.open('rb'))  # ← No try/except
```

**Problem**:
- If file is corrupted or unreadable, `FileResponse` will crash
- Need try/except wrapper
- Example:
  ```python
  try:
      response = FileResponse(local_path.open('rb'))
  except (IOError, OSError) as e:
      return JsonResponse({'error': f'Impossible de lire le fichier: {e}'}, status=500)
  ```

---

### **ISSUE #7: Supabase File NOT Downloaded if Local Check Fails**
**Severity**: 🔴 CRITICAL
**Location**: Lines 1290-1295

```python
if file_url.startswith('/media/'):
    local_path = BASE_DIR / file_url.lstrip('/')
    if not local_path.exists():
        return JsonResponse({'error': 'Fichier non trouvé'}, status=404)  # ← STOPS HERE
    response = FileResponse(local_path.open('rb'))
    return response  # ← RETURNS EARLY

# ↓ NEVER REACHES HERE for local files
file_response = requests.get(file_url)
```

**Problem**:
- If file is stored locally but missing from disk, download fails
- Should have fallback: check Supabase as backup
- OR restore file from Supabase backup

**Example**: During migration or file system issue, local file deleted but DB still has `/media/...` URL

---

### **ISSUE #8: Session Auth vs API Token Auth**
**Severity**: 🟡 MEDIUM
**Location**: Lines 1277 (download), 1302 (version download)

```python
@login_required_api
def api_fiche_download(request, fiche_id):
```

**Decorator Definition** (Lines 781-800):
```python
def login_required_api(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token:
            try:
                user = supabase.auth.get_user(token)
                if user:
                    request.user_id = user.user.id
                    request.user_email = user.user.email
                    return view_func(request, *args, **kwargs)
            except Exception:
                pass
        
        user_id = request.session.get('user_id')
        if user_id:
            # ✅ Session-based auth works
            return view_func(request, *args, **kwargs)
        
        return JsonResponse({'error': 'Authentification requise'}, status=401)
    return wrapper
```

**Problem**:
- If user downloads via SPA (JavaScript fetch), must include `Authorization: Bearer {token}` header
- OR be in same session as login
- **Missing**: No CORS headers for cross-origin requests

---

## 📊 SUMMARY TABLE

| Component | Status | Issue |
|-----------|--------|-------|
| **Local Download** | ✅ Works | Path resolution correct IF file exists |
| **Remote Download** | ✅ Works | Supabase proxy works |
| **Local Path Storage** | ✅ Working | 4 files in `/media/uploads/` |
| **URL Generation** | ✅ Correct | UUID prefix prevents collisions |
| **PDF Iframe Embed** | ⚠️ May fail | Needs CORS verification |
| **File Validation** | ❌ Missing | No type check on download |
| **Error Handling** | ⚠️ Minimal | File read errors not caught |
| **Fallback Logic** | ❌ Missing | No backup if local file missing |
| **Filename Encoding** | ❌ Missing | Non-ASCII filenames will break |
| **Preview on Version** | ❌ Missing | Versions don't generate previews |

---

## 🔧 RECOMMENDED FIXES

### Fix #1: Robust Local File Download with Fallback
```python
@login_required_api
def api_fiche_download(request, fiche_id):
    try:
        response = supabase.table('fiches').select('file_url, file_name, file_type').eq('id', fiche_id).execute()
        if not response.data or not response.data[0].get('file_url'):
            return JsonResponse({'error': 'Fichier non trouvé'}, status=404)
        
        fiche = response.data[0]
        file_url = fiche['file_url']
        file_name = fiche.get('file_name', 'document')
        file_type = fiche.get('file_type', 'application/octet-stream')
        
        # Try local first
        if file_url.startswith('/media/'):
            local_path = BASE_DIR / file_url.lstrip('/')
            try:
                response = FileResponse(local_path.open('rb'), content_type=file_type)
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
            except (IOError, OSError) as e:
                # Fallback to Supabase if local file missing
                print(f"Local file missing, trying remote: {e}")
                # Continue to remote download below
        
        # Remote file or fallback
        file_response = requests.get(file_url, timeout=30)
        if file_response.status_code != 200:
            return JsonResponse({'error': 'Fichier non accessible'}, status=500)
        
        response = HttpResponse(file_response.content, content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### Fix #2: PDF.js Library Instead of iframe
```javascript
async function viewFiche(id) {
    const data = await fetch(`/api/fiches/${id}/view/`).then(r => r.json());
    
    if (data.file_type?.includes('pdf')) {
        // Use PDF.js instead of iframe
        html = `
            <div id="pdf-viewer" style="height: 600px; border-radius: var(--radius);">
                <iframe src="/pdfjs/web/viewer.html?file=${encodeURIComponent(data.file_url)}" 
                        style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
        `;
    }
}
```

### Fix #3: Version Preview Generation
```python
@login_required_api
@csrf_exempt
@require_http_methods(["POST"])
def api_fiche_version(request, fiche_id):
    # ... existing code ...
    
    # Generate preview for version too!
    preview = generate_file_preview(file_data, file_type)
    
    version_data = {
        'fiche_id': fiche_id,
        'version': new_version,
        'file_url': upload_result['url'],
        'file_name': upload_result['name'],
        'file_preview': json.dumps(preview) if preview else None,  # ← ADD THIS
        'comment': request.POST.get('comment', ''),
        'author_id': request.user_id,
    }
```

---

## 🎯 CURRENT STATE: `/media/uploads/`

**4 files stored locally:**
- 15daa714_ThinkPad_E14_Gen_7_Intel_Spec.pdf
- 4d2c6dc8_ThinkPad_E14_Gen_7_Intel_Spec.pdf
- 6f1bbe87_ThinkPad_E14_Gen_7_Intel_Spec.pdf
- fe7db809_ThinkPad_E14_Gen_7_Intel_Spec.pdf

**Status**: ✅ Files ARE being stored correctly
**Issue**: Need to verify they can be downloaded/viewed correctly

