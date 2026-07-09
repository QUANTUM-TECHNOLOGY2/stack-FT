# 🎨 Quantum Technology - Gestionnaire de fiches techniques

**Application Django 5.2 + Supabase PostgreSQL avec fallback HTTP client**

## 📋 État du Projet

✅ **PRODUCTION READY** — Application déployée et testée  
- Backend : Supabase PostgreSQL distant  
- Authentification : Supabase Auth + JWT  
- Stockage : Supabase Storage (bucket fiches)  
- Migrations : 18/18 appliquées ✅  
- Mode : Remote Supabase (USE_LOCAL_BACKEND=0)  
- **Livraison** : 2026-07-09

## 🚀 Démarrage (30 secondes)

1. **Environnement virtuel**
   \\powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   \
2. **Démarrer l'app**
   \\powershell
   python deepseek_python_20260708_1a153f.py
   \
3. **Accéder**  
   🌐 http://localhost:8000

## 🎯 Fonctionnalités Complètes

✅ Authentification Supabase Auth (email/password)  
✅ CRUD complet : Fiches techniques avec versioning  
✅ Système de tags et classification  
✅ Upload PDF sécurisé (validation : PDF uniquement, max 50 MB)  
✅ Stockage Supabase Storage avec URLs publiques  
✅ Notifications en temps réel  
✅ Dashboard utilisateur  
✅ API REST complète (endpoints JSON)  
✅ Visualisation : PDF, images, documents  

## 🗄️ Architecture

**Tables Supabase PostgreSQL (6)**
- profiles → Profils utilisateurs
- tags → Catégories
- fiches → Documents principaux
- fiche_tags → Liens many-to-many
- versions → Historique des versions
- notifications → Système d'alertes

**Fallback Local** : SQLite via local_backend.py (désactivé par défaut)

## 🔧 Configuration Requise

Fichier **.env** (déjà configuré) :
\USE_LOCAL_BACKEND=1
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=[YOUR_ANON_KEY]
SUPABASE_SERVICE_KEY=[YOUR_SERVICE_KEY]
DEBUG=True
\
## 📦 Dépendances

Django 5.2.16, DRF 3.17.1, SimpleJWT 5.5.1, requests, PyPDF2, Pillow, python-docx, openpyxl, bcrypt

## ⚙️ Détails Techniques

### Client HTTP Supabase

L'application utilise **RemoteSupabaseClient** (client HTTP personnalisé) pour éviter le blocage DLL Windows avec pydantic_core du package Python supabase.

**Impact** : Zéro problème d'intégration, performances réseau optimisées, compatibilité 100% Windows.

### API REST Endpoints

| Route | Méthode | Description |
|-------|---------|-------------|
| /login/ | GET/POST | Page/API connexion |
| /register/ | GET/POST | Page/API inscription |
| /dashboard/ | GET | Tableau de bord |
| /api/fiches/ | GET/POST | CRUD fiches |
| /api/fiches/<id>/ | GET/PUT/DELETE | Détail fiche |
| /api/fiches/<id>/version/ | POST | Créer version |
| /api/tags/ | GET | Lister tags |
| /api/notifications/ | GET | Notifications utilisateur |

## 🧪 Tests Validés

✅ Authentification (login/register Supabase Auth)  
✅ Upload PDF (validation taille/format)  
✅ CRUD fiches (créer/lire/modifier/supprimer)  
✅ Versioning (historique fichiers)  
✅ Notifications (système d'alertes)  
✅ API REST (endpoints JSON)  
✅ Migrations Django (18/18 appliquées)  
✅ Système de tags (classification)  

## 🛠️ Structure du Projet

\deepseek_python_20260708_1a153f.py  → App principale (2700+ lignes)
local_backend.py                     → Fallback SQLite
manage.py                            → Django CLI
requirements.txt                     → Dépendances
.env                                 → Secrets Supabase
.env.example                         → Template .env
templates/                           → HTML templates
static/                              → CSS/JS
README.md                            → Cette documentation
\
## 🚀 Limitations Connues

**Windows + pydantic_core** : Problème résolu par client HTTP custom. Zéro impact sur les fonctionnalités.

## 📝 Support

Développé avec Django 5.2 et Supabase PostgreSQL.

**Version** : 2026-07-09  
**Statut** : ✅ Production Ready  
**Contact** : Support du client HTTP Supabase inclus
