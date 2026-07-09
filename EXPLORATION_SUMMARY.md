# 🔬 Quantum Project Exploration Report
**Date**: 2026-07-09  
**Status**: Analysis Complete  
**Issues Found**: 3 Critical, Multiple Warnings

---

## 📊 Project Structure Overview

### Architecture
| Component | Details |
|-----------|---------|
| **Type** | Single-file monolithic Django application |
| **Main File** | `deepseek_python_20260708_1a153f.py` (2,661 lines) |
| **Framework** | Django 5.2.16 + DRF 3.17.1 + SimpleJWT |
| **Database** | SQLite (local) + Supabase (remote fallback) |
| **Auth** | Supabase Auth + Local SQLite fallback |
| **Purpose** | Technical file management ("Fiches Techniques") |

### Backend Infrastructure
```
deepseek_python_20260708_1a153f.py (Settings + Views + Models + URLs)
├── local_backend.py (SQLite fallback)
├── data/app.sqlite3 (Local database)
├── media/uploads/ (File storage)
├── templates/ (HTML templates)
└── static/ (CSS/JS assets)
```

---

## 🗄️ Database Schema

### Tables
| Table | Purpose | Current Data |
|-------|---------|--------------|
| **fiches** | Technical documents/files | 2 records |
| **tags** | Categorization labels | 1 record ("PC") |
| **fiche_tags** | M2M relationships | **0 records** ⚠️ |
| **versions** | File version history | Unknown |
| **profiles** | User information | Unknown |
| **notifications** | System messages | Unknown |
| **auth_users** | Authentication (local) | Unknown |

### Current Data State
```
FICHES:
1. FT-2026-001: "LAPTOP LENOVO"
   - Category: ELECTRONIQUE
   - File: /media/uploads/uploads/15daa714_ThinkPad_E14_Gen_7...
   
2. FT-6ea48093: "LAPTOP LENOVO"
   - Category: (EMPTY)
   - File: /media/uploads/uploads/4d2c6dc8_ThinkPad_E14_Gen_7...

TAGS: 1 total
   - "PC"

FICHE_TAGS: 0 relationships (NOT LINKED!)
```

---

## 🎯 Key Features & Views

### Frontend Routes
```
/                        → Redirects to login
/login/                  → Login page
/register/              → Registration page
/dashboard/             → Main dashboard (file list)
/fiche/<fiche_id>/     → File detail view
/logout/                → Logout & session clear
```

### API Endpoints (`/api/*`)
```
Authentication:
  POST /api/auth/login/                          Login
  POST /api/auth/register/                       Register

File Management:
  GET  /api/fiches/                              List fiches (paginated, searchable)
  POST /api/fiches/create/                       Create new fiche
  GET  /api/fiches/<id>/                         Get fiche details
  PUT  /api/fiches/<id>/update/                  Update fiche metadata
  DELETE /api/fiches/<id>/delete/                Delete fiche
  POST /api/fiches/<id>/version/                 Add new version
  GET  /api/fiches/<id>/download/                Download file
  GET  /api/fiches/<id>/view/                    Get file preview

Tags & Notifications:
  GET  /api/tags/                                Get all tags
  GET  /api/notifications/                       Get notifications
  PUT  /api/notifications/<id>/read/             Mark as read
  GET  /api/stats/                               Get statistics
```

### Core Views (Python Functions)
```python
login_view()                    → Login/auth
register_view()                 → Registration/account creation
dashboard_view()                → Dashboard display
fiche_detail_view(fiche_id)     → Single fiche view
api_fiches_list()               → List fiches with filters
api_fiche_create()              → File upload & creation
api_fiche_detail(fiche_id)      → Fiche metadata API
api_fiches_update(fiche_id)     → Update metadata
api_fiches_delete(fiche_id)     → Delete fiche
api_fiche_version(fiche_id)     → Version management
api_fiche_download(fiche_id)    → File download
api_fiche_view(fiche_id)        → Preview generation
```

---

## 🔍 Search & Filtering Logic

### Search Implementation
**Location**: `api_fiches_list()` (line ~870)

**Search Fields**:
- Reference (exact match)
- Name (text search)
- Description (text search)
- Manufacturer (text search)

**Search Method**: `.or_()` with `.ilike.%search%` filters

**Query Parameters**:
```
GET /api/fiches/?search=laptop&category=ELECTRONIQUE&tag=PC&page=1
```

**Pagination**: 20 items per page

**Ordering**: By `created_at DESC` (newest first)

**⚠️ Issue**: Complex `.or_()` query might not work properly with SQLite backend

---

## 📤 File Import Logic

### File Upload Flow (`api_fiche_create`)
```
1. Receive multipart form data
   ├── file (PDF only, max 50MB)
   ├── name (required)
   ├── reference (optional, auto-generated)
   ├── description
   ├── category
   ├── manufacturer
   ├── version
   └── tags (comma-separated)

2. Validate file
   ├── Check if PDF (by extension or MIME type)
   └── Check size < 50MB

3. Generate preview (optional)
   ├── PDF: Extract pages count + first 1000 chars
   ├── Images: Store dimensions
   ├── Word: Extract paragraphs
   ├── Excel: Count sheets
   └── Text: Extract first 2000 chars

4. Upload to storage
   ├── If local: /media/uploads/[UUID]_filename
   └── If Supabase: Storage bucket "fiches"

5. Save to database
   ├── Create fiche record
   ├── Create tags if needed
   ├── Create fiche_tags relationships
   └── Create notification

6. Return JSON response with fiche ID
```

### File Validation
```python
- Only PDF files allowed
- Maximum 50 MB
- Extensions checked: .pdf
- MIME types checked: application/pdf
```

---

## 🚨 CRITICAL ISSUES FOUND

### ❌ Issue #1: FicheTechnique NameError (BLOCKING)
**Severity**: 🔴 CRITICAL - Prevents fiches from displaying

**Location**: Line 903 in `api_fiches_list()`

**Error Code**:
```python
'category_display': dict(FicheTechnique.CATEGORY_CHOICES).get(...)
                         ^^^^^^^^^^^^^^  # NOT DEFINED!
```

**Error Message**:
```
NameError: name 'FicheTechnique' is not defined
```

**Debug Log Evidence**:
```
[API_FICHES] Exception: name 'FicheTechnique' is not defined
[API_FICHES] Traceback:
  File "deepseek_python_20260708_1a153f.py", line 903
    'category_display': dict(FicheTechnique.CATEGORY_CHOICES)
                                    ^^^^^^^^^^^^^^
NameError: name 'FicheTechnique' is not defined
```

**Impact**:
- ❌ API returns 500 error when listing fiches
- ❌ Dashboard cannot display any files
- ❌ Search functionality broken
- ❌ File list completely inaccessible

**Root Cause**: 
The code references a Django model class `FicheTechnique` that doesn't exist. No Django models are defined in this single-file app.

**Solution**: 
Remove the problematic line or simplify to just use `fiche.get('category', 'Non catégorisé')`

---

### ⚠️ Issue #2: Tag Associations Not Working
**Severity**: 🟡 HIGH - Tags cannot be linked to files

**Location**: Database state

**Evidence**:
```
Tags in database: 1 ("PC")
Fiche_tags relationships: 0 (ZERO!)
```

**Problem**:
- When creating fiches, tags are not being associated with fiche_tags table
- The relationship table remains empty despite tag creation logic existing

**Possible Causes**:
1. Tag linking code in `api_fiche_create()` not executing
2. Transaction/commit issue in local SQLite backend
3. Foreign key constraints failing silently

**Impact**:
- ❌ No fiche appears with tags
- ❌ Tag filtering returns no results
- ❌ Tag suggestions won't work

---

### ⚠️ Issue #3: Category Display Inconsistency
**Severity**: 🟡 MEDIUM - Incomplete data

**Location**: Database/API

**Evidence**:
```
Fiche 1: category = "ELECTRONIQUE"
Fiche 2: category = NULL/empty
```

**Problem**:
- Not all fiches have categories assigned
- Second fiche created without category despite field existing

**Impact**:
- ❌ Category filtering may exclude items
- ⚠️ Dashboard shows "Non catégorisé" fallback
- ⚠️ Stats might not count correctly

---

## 📁 File Management Issues

### File Path Handling
**Potential Issue**: Mixed file URL formats

```
Stored URLs:
  - Local: /media/uploads/uploads/[UUID]_filename
  - Remote: https://[project].supabase.co/storage/v1/object/public/fiches/[path]
```

**Problem**: 
- Local paths may not be accessible if served incorrectly
- Mixed formats in same database

**In Dashboard/API**:
```javascript
// Gets file URL from database
const file_url = fiche.file_url;  // Could be /media/... or https://...
// Uses directly in iframe/image tag
<iframe src="${file_url}"></iframe>  // May not have proper CORS/access
```

---

## 📊 Search Functionality Analysis

### How Search Works
```python
def api_fiches_list(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')
    
    query = supabase.table('fiches').select('*')
    
    if search:
        # Using .or_() with ilike (case-insensitive like)
        query = query.or_(
            f"reference.ilike.%{search}%," +
            f"name.ilike.%{search}%," +
            f"description.ilike.%{search}%," +
            f"manufacturer.ilike.%{search}%"
        )
    
    if category:
        query = query.eq('category', category)
    
    # Pagination
    offset = (page - 1) * per_page
    response = query.range(offset, offset + per_page - 1)\
                    .order('created_at', desc=True)\
                    .execute()
```

### Issues
⚠️ **SQLite Limitation**: `.or_()` with `.ilike()` syntax is **Supabase-specific**
- May not work with local SQLite backend
- SQLite uses different operators: `LIKE`, `%pattern%`
- This could cause search to fail silently or throw errors

⚠️ **Tag Filter Not Implemented**: 
```python
if tag:  # This parameter is received but NOT used in the query!
    # Missing implementation
```

---

## 🛡️ Dashboard Display Pipeline

### How Files Appear on Dashboard
```
1. User loads /dashboard/
   ├── Backend: require_app_login decorator checks session
   ├── Renders: dashboard.html template
   └── Triggers: loadFiches() JavaScript function

2. JavaScript: loadFiches()
   ├── Calls: GET /api/fiches/?page=1
   ├── Expects: JSON array of fiches
   └── On Error: Shows error toast

3. API: /api/fiches/ 
   ├── Query database
   ├── Fetch tags for each fiche
   ├── Build response array
   ├── **BUG**: Crashes on line 903 with FicheTechnique error
   └── Returns: 500 error to frontend

4. Frontend receives error
   ├── Shows error message
   ├── No fiches displayed
   └── Dashboard remains empty
```

### Why Files Don't Show Up
```
┌─ FicheTechnique NameError ─┐
│                            │
├─ API returns 500 error    │
│                            │
├─ loadFiches() catches error│
│                            │
├─ showToast('Error', 'error')
│                            │
└─ Dashboard remains EMPTY   ┘
```

---

## 📋 Template/Frontend Analysis

### Dashboard Template (`dashboard.html`)
```html
<script>
  async function loadFiches() {
    try {
      const response = await fetch('/api/fiches/');
      const data = await response.json();
      
      if (!response.ok) throw new Error(data.error);
      
      renderFiches(data.results);  // Renders fiche cards
    } catch (error) {
      showToast(error.message, 'error');  // Shows error
    }
  }
  
  // Renders as cards with:
  // - Name, reference, version
  // - Category, manufacturer
  // - Tags
  // - Buttons: View, Download, Edit, Delete, History
```

### File Detail Template (`fiche_detail.html`)
```html
<!-- Shows single fiche with: -->
- Title & reference
- Description
- Manufacturer & author info
- Tags
- File viewer (iframe/image/text)
- Version history
- Download button
```

---

## 🔧 Code Quality Observations

### Good Practices
✅ Logging to debug files (`api_fiches_debug.log`, etc.)  
✅ Try-catch error handling around API calls  
✅ CSRF token handling  
✅ Session-based authentication  
✅ Input validation (file type, size)  
✅ Responsive design  

### Issues
❌ Single-file monolithic architecture (2661 lines)  
❌ Incomplete error handling  
❌ Unused imports/libraries  
❌ Hardcoded credentials structure  
❌ Backend-agnostic query syntax issues  
❌ No unit tests visible  
❌ File URL inconsistency  

---

## 📝 Summary Table

| Aspect | Status | Notes |
|--------|--------|-------|
| **Django Setup** | ✅ OK | Properly configured |
| **Database** | ✅ OK | SQLite working, tables created |
| **Authentication** | ✅ OK | Login/register functional |
| **File Upload** | ✅ OK | API endpoint exists, validation present |
| **Database Queries** | ❌ BROKEN | FicheTechnique error blocks API |
| **Search** | ⚠️ PARTIAL | May not work with SQLite |
| **Tag System** | ⚠️ BROKEN | No fiche_tags relationships |
| **Dashboard Display** | ❌ BROKEN | API error prevents data loading |
| **File Download** | ✅ OK | Logic looks correct |
| **File Preview** | ✅ OK | Supports PDF, images, text, Word, Excel |
| **Notifications** | ✅ OK | System exists |
| **UI/UX** | ✅ OK | Responsive templates |

---

## 🎯 Recommendations

### Immediate Fixes (Critical)
1. **Remove FicheTechnique reference** in `api_fiches_list()` line 903
2. **Fix tag associations** - Implement fiche_tags linking during import
3. **Test search queries** with SQLite backend

### Short-term Improvements
4. Implement tag filtering (currently received but unused)
5. Verify file URL accessibility and serving
6. Add proper error responses instead of silent failures

### Long-term Refactoring
7. Break monolithic file into separate modules
8. Add comprehensive error handling
9. Add unit/integration tests
10. Document API responses properly

---

## 📚 File Listing

| File | Purpose | Lines |
|------|---------|-------|
| `deepseek_python_20260708_1a153f.py` | Main app (settings + views + URLs) | 2,661 |
| `local_backend.py` | SQLite fallback implementation | 300+ |
| `manage.py` | Django CLI wrapper | 11 |
| `templates/dashboard.html` | Main file list view | Embedded |
| `templates/fiche_detail.html` | File detail view | Embedded |
| `templates/login.html` | Login form | Embedded |
| `templates/register.html` | Registration form | Embedded |
| `templates/base.html` | Base template | Embedded |

---

**End of Report**
