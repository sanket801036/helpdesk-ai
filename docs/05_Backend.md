# 05 — Backend

> **Phase 3 — Backend Setup (VERIFIED ✅).** FastAPI skeleton ready. Migration test pass.
> Stack: **MySQL** (no Docker, no Redis). AI = **Hugging Face**. Tables prefix: `helpdesk_`.

---

## 1. Setup (aapke laptop par)

```bash
git clone https://github.com/sanket801036/helpdesk-ai.git
cd helpdesk-ai/backend

python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt

# env
copy ..\.env.example .env         # .env me apna DATABASE_URL + HF_API_KEY bharo
# DATABASE_URL=mysql+aiomysql://erp_user:root@localhost:3306/erp?charset=utf8mb4

# migration (tables banega -> helpdesk_users)
alembic upgrade head

# run
uvicorn app.main:app --reload
```
- Root: http://localhost:8000/
- Swagger: http://localhost:8000/api/v1/docs
- Health: http://localhost:8000/api/v1/health  → `{status: ok, db: true}`

> ⚠️ **Note:** Ye backend jis machine par chalega usi se MySQL reachable hona chahiye.
> Aapke laptop par MySQL local hai to `localhost` use karo (ya `192.168.1.64`).

---

## 2. Stack (updated)

| Cheez | Value |
|-------|-------|
| DB | **MySQL** (driver: `aiomysql`) |
| Migrations | Alembic (async) |
| AI | **Hugging Face Inference API** |
| Embeddings | JSON file (RAG), numpy cosine — no pgvector |
| Redis | ❌ nahi (hata diya) |
| Docker | ❌ abhi nahi |
| Table prefix | `helpdesk_` (existing ERP tables safe) |

---

## 3. Folder Structure

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
└── Dockerfile                   # (optional, abhi use nahi)
```

---

## 4. Verification (Phase 3 done)
- ✅ App imports (saare modules load)
- ✅ `pytest` green (endpoint responds)
- ✅ `alembic upgrade head` → `helpdesk_users` table + unique email index bani
- ✅ `alembic current` → `0001_initial (head)`

(Ye SQLite par verify hua — kyunki build-machine se aapka MySQL reachable nahi.
Aapke laptop par same migration MySQL `erp` DB me `helpdesk_users` banayega.)

---

## 5. Next
**Phase 4 — Frontend Setup** (React + TS + Tailwind).
