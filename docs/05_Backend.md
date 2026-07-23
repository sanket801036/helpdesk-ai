# 05 — Backend

> **Phase 3 — Backend Setup.** FastAPI skeleton ready (config, async DB, JWT, Redis,
> Alembic, `/health`, dummy `User` model). Feature modules Phase 5+ me aayenge.

---

## 1. Setup (local)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # win: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env        # values bharo (ya root .env use karo)

# migrations
alembic revision --autogenerate -m "create users table"
alembic upgrade head

# run
uvicorn app.main:app --reload
```
- API root: http://localhost:8000/
- Swagger: http://localhost:8000/api/v1/docs
- Health: http://localhost:8000/api/v1/health

Docker se: `docker-compose up --build` (backend + db + redis).

---

## 2. Folder Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app factory
│   ├── core/
│   │   ├── config.py            # settings (pydantic-settings)
│   │   ├── database.py          # async engine, session, Base, get_db
│   │   ├── security.py          # password hash + JWT
│   │   └── redis_client.py      # redis connection + ping
│   ├── models/
│   │   ├── mixins.py            # UUIDMixin, TimestampMixin
│   │   └── user.py              # User model (dummy/base)
│   └── api/
│       └── v1/
│           ├── router.py        # aggregates routers
│           └── routers/
│               └── health.py    # /health (db + redis check)
├── alembic/                     # migrations env
├── alembic.ini
├── tests/
│   └── test_health.py
├── requirements.txt
└── Dockerfile
```

---

## 3. Core Building Blocks

| File | Kya |
|------|-----|
| `core/config.py` | Env-driven settings, `settings` singleton |
| `core/database.py` | Async SQLAlchemy engine + `get_db()` dependency + `Base` |
| `core/security.py` | `hash_password`, `verify_password`, JWT create/decode |
| `core/redis_client.py` | Async Redis client + `ping_redis()` |
| `models/mixins.py` | UUID PK + `created_at`/`updated_at` (convention §7) |
| `models/user.py` | `User` + `UserRole` enum — proves DB/migration |
| `api/v1/routers/health.py` | `/health` → `{status, db, redis}` |
| `main.py` | app factory, CORS, router mount, `/` root |

---

## 4. Layering (recap)
`Router → Service → Repository → Model` (MASTER_GUIDE §4).
Abhi sirf skeleton; services/repositories Phase 5 se add honge.

---

## 5. Migrations (Alembic)
- Async `env.py` — DB URL `settings.DATABASE_URL` se.
- Models `alembic/env.py` me import hote hain (metadata detect ke liye).
- Flow: `alembic revision --autogenerate -m "..."` → `alembic upgrade head`.
- pgvector extension pehli real migration me: `CREATE EXTENSION IF NOT EXISTS vector;`

---

## 6. Testing
- `pytest` — abhi ek smoke test (`test_health.py` root endpoint).
- DB/Redis integration tests Phase 14 me.

---

## 7. Next
**Phase 4 — Frontend Setup** (React + TS + Tailwind + routing + api client).
