# 05 — Backend

> **Phase 3 — Backend Setup (VERIFIED ✅).** FastAPI skeleton. Migration test pass.
> Stack: **PostgreSQL (Docker)**, no Redis. AI = **Hugging Face**. Tables prefix: `helpdesk_`.

---

## 1. Run (Docker — recommended)

Laptop par (Docker installed hona chahiye):
```bash
git clone https://github.com/sanket801036/helpdesk-ai.git
cd helpdesk-ai
docker-compose up --build
```
Bas! Ye khud:
- PostgreSQL utha dega (user/pass/db = helpdesk, credentials pre-set)
- migration chala dega → `helpdesk_users` table banega
- backend start kar dega

Check:
- Root: http://localhost:8000/
- Swagger: http://localhost:8000/api/v1/docs
- Health: http://localhost:8000/api/v1/health → `{status: ok, db: true}`

Band karna: `Ctrl+C`, phir `docker-compose down` (data rakhne ke liye) ya
`docker-compose down -v` (DB data bhi delete).

---

## 2. Run (bina Docker — optional)
Agar apna local Postgres use karna ho:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy ..\.env.example .env       # DATABASE_URL apne postgres ka daalo
alembic upgrade head
python -m uvicorn app.main:app --reload   # NOTE: 'python -m' zaroori (venv use ho)
```

---

## 3. Stack

| Cheez | Value |
|-------|-------|
| DB | **PostgreSQL 16** (Docker, pgvector image) |
| Driver | `asyncpg` |
| Migrations | Alembic (async) |
| AI | **Hugging Face Inference API** |
| Redis | ❌ nahi |
| Table prefix | `helpdesk_` |

---

## 4. Folder Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app factory
│   ├── core/
│   │   ├── config.py            # settings + TABLE_PREFIX
│   │   ├── database.py          # async engine, session, Base, get_db
│   │   └── security.py          # password hash + JWT
│   ├── models/
│   │   ├── mixins.py            # UUID (generic) + timestamps
│   │   └── user.py              # User -> helpdesk_users
│   └── api/v1/
│       ├── router.py
│       └── routers/health.py    # /health (db check)
├── alembic/
│   └── versions/0001_initial_helpdesk_users.py
├── alembic.ini
├── tests/test_health.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

---

## 5. Verification (Phase 3 done)
- ✅ App imports (saare modules load)
- ✅ `pytest` green (endpoint responds)
- ✅ `alembic upgrade head` → `helpdesk_users` table + unique email index
- ✅ `alembic current` → `0001_initial (head)`

---

## 6. Next
**Phase 4 — Frontend Setup** (React + TS + Tailwind).
