import os
import sqlite3
import uuid
import json
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime

try:
    import bcrypt
except Exception:  # pragma: no cover
    bcrypt = None


class LocalBackend:
    def __init__(self, base_dir: Path, media_root: Path):
        self.base_dir = base_dir
        self.media_root = media_root
        self.data_dir = base_dir / "data"
        self.db_path = self.data_dir / "app.sqlite3"
        self.storage_root = media_root / "uploads"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self.storage = LocalStorage(self)
        self.auth = LocalAuth(self)

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT,
            avatar_url TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#293462',
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS fiches (
            id TEXT PRIMARY KEY,
            reference TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            manufacturer TEXT,
            version TEXT DEFAULT '1.0',
            file_url TEXT,
            file_name TEXT,
            file_size INTEGER,
            file_type TEXT,
            file_preview TEXT,
            author_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS fiche_tags (
            fiche_id TEXT NOT NULL,
            tag_id TEXT NOT NULL,
            PRIMARY KEY (fiche_id, tag_id)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS versions (
            id TEXT PRIMARY KEY,
            fiche_id TEXT NOT NULL,
            version TEXT NOT NULL,
            file_url TEXT,
            file_name TEXT,
            comment TEXT,
            author_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            recipient_id TEXT NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            fiche_id TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS auth_users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            access_token TEXT,
            refresh_token TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def table(self, name: str):
        return LocalTable(self, name)

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


class LocalTable:
    def __init__(self, backend: LocalBackend, table_name: str):
        self.backend = backend
        self.table_name = table_name
        self._action = "select"
        self._data = None
        self._filters = []
        self._order_by = None
        self._order_desc = False
        self._range_start = None
        self._range_end = None
        self._limit = None
        self._select_fields = None
        self._count = False

    def select(self, *fields, **kwargs):
        self._action = "select"
        self._select_fields = list(fields)
        self._count = kwargs.get("count") == "exact"
        return self

    def insert(self, data):
        self._action = "insert"
        self._data = data
        return self

    def update(self, data):
        self._action = "update"
        self._data = data
        return self

    def delete(self):
        self._action = "delete"
        return self

    def eq(self, column, value):
        self._filters.append((column, "=", value))
        return self

    def or_(self, expression: str):
        self._filters.append(("__or__", expression, None))
        return self

    def order(self, column, desc=False):
        self._order_by = column
        self._order_desc = desc
        return self

    def range(self, start, end):
        self._range_start = start
        self._range_end = end
        return self

    def limit(self, value):
        self._limit = value
        return self

    def execute(self):
        if self._action == "insert":
            return self._insert()
        if self._action == "update":
            return self._update()
        if self._action == "delete":
            return self._delete()
        return self._select()

    def _insert(self):
        conn = self.backend._conn()
        data = dict(self._data or {})
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        if self.table_name == "profiles" and "created_at" not in data:
            data["created_at"] = now
        if self.table_name == "profiles" and "updated_at" not in data:
            data["updated_at"] = now
        if self.table_name == "fiches" and "created_at" not in data:
            data["created_at"] = now
        if self.table_name == "fiches" and "updated_at" not in data:
            data["updated_at"] = now
        if self.table_name == "notifications" and "created_at" not in data:
            data["created_at"] = now
        if self.table_name == "versions" and "created_at" not in data:
            data["created_at"] = now
        if self.table_name == "tags" and "created_at" not in data:
            data["created_at"] = now
        columns = list(data.keys())
        placeholders = ", ".join(["?" for _ in columns])
        values = [self._serialize_value(data[c]) for c in columns]
        sql = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor = conn.execute(sql, values)
        conn.commit()
        row = conn.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (data["id"],)).fetchone()
        conn.close()
        return SimpleNamespace(data=[dict(row)] if row else [], count=1)

    def _update(self):
        conn = self.backend._conn()
        data = dict(self._data or {})
        if not data:
            conn.close()
            return SimpleNamespace(data=[], count=0)
        assignments = ", ".join([f"{column} = ?" for column in data.keys()])
        values = [self._serialize_value(data[column]) for column in data.keys()]
        sql = f"UPDATE {self.table_name} SET {assignments}"
        where_sql, where_params = self._build_where_clause()
        if where_sql:
            sql += f" WHERE {where_sql}"
            values.extend(where_params)
        conn.execute(sql, values)
        conn.commit()
        conn.close()
        return SimpleNamespace(data=[], count=0)

    def _delete(self):
        conn = self.backend._conn()
        sql = f"DELETE FROM {self.table_name}"
        where_sql, where_params = self._build_where_clause()
        if where_sql:
            sql += f" WHERE {where_sql}"
        conn.execute(sql, where_params)
        conn.commit()
        conn.close()
        return SimpleNamespace(data=[], count=0)

    def _select(self):
        conn = self.backend._conn()
        if self._count:
            sql = f"SELECT COUNT(*) AS count FROM {self.table_name}"
            where_sql, where_params = self._build_where_clause()
            if where_sql:
                sql += f" WHERE {where_sql}"
            row = conn.execute(sql, where_params).fetchone()
            conn.close()
            return SimpleNamespace(data=[], count=int(row["count"]) if row else 0)

        columns = self._select_fields or ["*"]
        sql = f"SELECT * FROM {self.table_name}"
        where_sql, where_params = self._build_where_clause()
        if where_sql:
            sql += f" WHERE {where_sql}"
        if self._order_by:
            sql += f" ORDER BY {self._order_by} {'DESC' if self._order_desc else 'ASC'}"
        if self._limit is not None:
            sql += " LIMIT ?"
            where_params.append(self._limit)
        if self._range_start is not None and self._range_end is not None:
            sql += " LIMIT ? OFFSET ?"
            where_params.extend([self._range_end - self._range_start + 1, self._range_start])
        rows = conn.execute(sql, where_params).fetchall()
        conn.close()
        data = []
        for row in rows:
            item = dict(row)
            if self._is_profiles_join(columns):
                profile_id = item.get("author_id")
                if profile_id:
                    profile = self.backend.table("profiles").select("*").eq("id", profile_id).execute()
                    item["profiles"] = dict(profile.data[0]) if profile.data else {}
            data.append(item)
        return SimpleNamespace(data=data, count=len(data))

    def _build_where_clause(self):
        clauses = []
        params = []
        for filter_part in self._filters:
            if filter_part[0] == "__or__":
                expr = filter_part[1]
                or_clauses = []
                for segment in expr.split(","):
                    segment = segment.strip()
                    if not segment:
                        continue
                    if ".ilike." in segment:
                        field, value = segment.split(".ilike.", 1)
                        value = value.strip("%")
                        or_clauses.append(f"{field} LIKE ?")
                        params.append(f"%{value}%")
                if or_clauses:
                    clauses.append(f"({' OR '.join(or_clauses)})")
            else:
                column, operator, value = filter_part
                clauses.append(f"{column} {operator} ?")
                params.append(self._serialize_value(value))
        return " AND ".join(clauses), params

    def _serialize_value(self, value):
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        if isinstance(value, bool):
            return int(value)
        return value

    def _is_profiles_join(self, columns):
        return any("profiles(" in str(c) for c in columns)


class LocalAuth:
    def __init__(self, backend: LocalBackend):
        self.backend = backend

    def sign_up(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return SimpleNamespace(user=None, session=None)
        user_id = str(uuid.uuid4())
        password_hash = self._hash_password(password)
        conn = self.backend._conn()
        conn.execute(
            "INSERT INTO auth_users (id, email, password_hash, access_token, refresh_token) VALUES (?, ?, ?, ?, ?)",
            (user_id, email, password_hash, self._make_token(user_id), self._make_token(user_id, prefix="refresh")),
        )
        conn.commit()
        conn.close()
        return SimpleNamespace(
            user=SimpleNamespace(id=user_id, email=email),
            session=SimpleNamespace(access_token=self._make_token(user_id), refresh_token=self._make_token(user_id, prefix="refresh")),
        )

    def sign_in_with_password(self, data):
        email = data.get("email")
        password = data.get("password")
        conn = self.backend._conn()
        row = conn.execute("SELECT * FROM auth_users WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        # Debug logging
        log_file = open('login_debug.log', 'a')
        log_file.write(f"[LOGIN] Email: {email}\n")
        log_file.write(f"[LOGIN] Row found: {row is not None}\n")
        
        if not row:
            log_file.write(f"[LOGIN] User not found\n")
            log_file.close()
            return SimpleNamespace(user=None, session=None)
        
        password_check = self._check_password(password, row["password_hash"])
        log_file.write(f"[LOGIN] Password check result: {password_check}\n")
        log_file.write(f"[LOGIN] Stored hash type: {type(row['password_hash'])}\n")
        log_file.write(f"[LOGIN] Password provided: {'*' * len(password)}\n")
        log_file.close()
        
        if not password_check:
            return SimpleNamespace(user=None, session=None)
        return SimpleNamespace(
            user=SimpleNamespace(id=row["id"], email=row["email"]),
            session=SimpleNamespace(access_token=row["access_token"] or self._make_token(row["id"]), refresh_token=row["refresh_token"] or self._make_token(row["id"], prefix="refresh")),
        )

    def get_user(self, token):
        if not token:
            return None
        conn = self.backend._conn()
        row = conn.execute("SELECT * FROM auth_users WHERE access_token = ?", (token,)).fetchone()
        conn.close()
        if not row:
            return None
        return SimpleNamespace(user=SimpleNamespace(id=row["id"], email=row["email"]))

    def _hash_password(self, password):
        if bcrypt is not None:
            return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return password

    def _check_password(self, password, password_hash):
        if bcrypt is not None:
            try:
                return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
            except Exception:
                return False
        return password == password_hash

    def _make_token(self, user_id, prefix="access"):
        return f"{prefix}_{user_id}_{uuid.uuid4().hex[:16]}"


class LocalStorage:
    def __init__(self, backend: LocalBackend):
        self.backend = backend

    def from_(self, bucket_name: str):
        return LocalBucket(self.backend, bucket_name)


class LocalBucket:
    def __init__(self, backend: LocalBackend, bucket_name: str):
        self.backend = backend
        self.bucket_name = bucket_name

    def upload(self, file_path, file_data, metadata=None):
        dest = self._resolve_path(file_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(file_data, str):
            dest.write_text(file_data, encoding="utf-8")
        else:
            dest.write_bytes(file_data)
        return True

    def get_public_url(self, file_path):
        return f"/media/uploads/{self._clean_path(file_path)}"

    def remove(self, paths):
        for path in paths:
            dest = self._resolve_path(path)
            if dest.exists():
                dest.unlink()
        return True

    def _clean_path(self, file_path):
        value = file_path.replace("\\", "/")
        return value.lstrip("/")

    def _resolve_path(self, file_path):
        value = self._clean_path(file_path)
        if value.startswith("uploads/"):
            value = value[len("uploads/"):]
        return self.backend.storage_root / value


def create_local_backend(base_dir: Path, media_root: Path):
    return LocalBackend(base_dir, media_root)
