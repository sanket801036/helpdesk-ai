# PROJECT MASTER GUIDE — Helpdesk AI Platform

> **Yeh file project ka "constitution" hai.**
> Har AI session / har developer isse follow karega. Kabhi bhi "pura project bana do"
> mat bolo. Hamesha: **ek phase → implement → test → commit → push → next phase.**
>
> AI ko prompt dete waqt hamesha likho:
> **"PROJECT_MASTER_GUIDE.md follow karo aur sirf Phase X implement karo."**

---

## 0. Table of Contents

1. Project Vision & Scope
2. Tech Stack (final)
3. High-Level Architecture
4. Folder Structure (backend + frontend)
5. Coding Standards
6. API Conventions
7. Database Conventions
8. Git Conventions
9. Testing Checklist
10. Deployment Checklist
11. README Checklist
12. Security Checklist
13. Standard Phase Template (har phase isi format me)
14. Full 20-Phase Roadmap + ready prompts
15. docs/ structure
16. Definition of Done (DoD)

---

## 1. Project Vision & Scope

**Product:** AI-powered Customer Support / Helpdesk Platform.

**One-line:** Ek platform jahan customers ticket raise karein, agents unhe manage karein,
live chat ho, aur ek AI assistant (RAG-based) knowledge base se turant jawaab de.

**Core value:** Support team ka time bachana — AI pehle se jawaab suggest kare, common
sawaal khud handle kare, aur agents ko sirf zaroori tickets par focus karne de.

**In scope (v1.0):**
- Authentication + RBAC (Admin / Agent / Customer)
- Customer management
- Ticket management (create, assign, status, priority, comments)
- Live chat (agent ↔ customer)
- Knowledge Base (articles)
- AI Module (Ollama + Embeddings + RAG + streaming answers)
- Dashboard + Analytics
- Notifications
- Docker + CI/CD + Deployment + Docs

**Out of scope (v1.0):** billing/payments, multi-language UI, mobile app, telephony/voice.

**User Roles:**
| Role | Kya kar sakta hai |
|------|-------------------|
| Admin | Sab kuch — users, roles, settings, analytics, KB manage |
| Agent | Tickets handle, live chat, KB padhna, AI assist use karna |
| Customer | Ticket raise, apne tickets dekhna, chat, KB search |

---

## 2. Tech Stack (final — isse mat badlo bina reason ke)

**Backend**
- Language: Python 3.11+
- Framework: **FastAPI**
- ORM: **SQLAlchemy 2.x** (async)
- Migrations: **Alembic**
- DB: **PostgreSQL 16**
- Cache / queue / pub-sub: **Redis 7**
- Auth: **JWT** (access + refresh), password hashing = bcrypt/argon2
- Validation: Pydantic v2
- Async server: Uvicorn (+ Gunicorn workers in prod)

**Frontend**
- **React 18 + TypeScript**
- Build: Vite
- Styling: **Tailwind CSS**
- Routing: React Router
- State/Data: TanStack Query (server state) + Zustand/Context (UI state)
- Forms: React Hook Form + Zod
- HTTP: Axios (interceptors for token refresh)

**AI Module**
- Default: **Ollama** (local LLM) — e.g. `llama3.1` / `qwen2.5`
- Embeddings: Ollama embeddings (e.g. `nomic-embed-text`)
- Vector store: **pgvector** (Postgres extension) — ek hi DB, kam moving parts
- Pattern: **RAG** (Retrieval Augmented Generation) with streaming
- **Provider abstraction:** ek `AIProvider` interface — kal ko Claude API par switch
  karna ho to sirf ek adapter add karna, baaki code change nahi.

**Infra / DevOps**
- Docker + docker-compose
- CI/CD: GitHub Actions
- Reverse proxy: Nginx (prod)
- Env management: `.env` files + `.env.example`

---

## 3. High-Level Architecture

```
                         ┌──────────────────────────┐
                         │        Frontend           │
                         │   React + TS + Tailwind   │
                         └────────────┬─────────────┘
                                      │ HTTPS / JSON (REST) + WebSocket (chat)
                                      ▼
                         ┌──────────────────────────┐
                         │        FastAPI            │
                         │  Routers → Services →     │
                         │  Repositories             │
                         └───┬───────────┬───────┬───┘
                             │           │       │
                   ┌─────────▼──┐  ┌─────▼────┐ ┌▼──────────┐
                   │ PostgreSQL │  │  Redis   │ │  AI Layer │
                   │ + pgvector │  │ cache/ws │ │  Ollama   │
                   └────────────┘  └──────────┘ │  + RAG    │
                                                 └───────────┘
```

**Layering rule (backend):**
`Router (HTTP)` → `Service (business logic)` → `Repository (DB access)` → `Model`.
Router me business logic mat likho. Repository ke bahar SQLAlchemy query mat karo.

---

## 4. Folder Structure

### Backend
```
backend/
├── app/
│   ├── main.py                # FastAPI app factory
│   ├── core/
│   │   ├── config.py          # settings (pydantic-settings)
│   │   ├── security.py        # JWT, hashing
│   │   ├── database.py        # engine, session
│   │   └── logging.py
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic request/response
│   ├── repositories/          # DB access layer
│   ├── services/              # business logic
│   ├── api/
│   │   └── v1/
│   │       ├── routers/       # auth.py, users.py, tickets.py ...
│   │       └── deps.py        # dependencies (get_current_user etc.)
│   ├── ai/                    # AIProvider, embeddings, rag, prompts
│   └── utils/
├── alembic/                   # migrations
├── tests/
├── requirements.txt / pyproject.toml
├── Dockerfile
└── .env.example
```

### Frontend
```
frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes/
│   ├── pages/
│   ├── components/            # reusable UI
│   ├── features/             # feature-based (auth, tickets, chat...)
│   ├── api/                   # axios client + endpoints
│   ├── hooks/
│   ├── store/                 # zustand stores
│   ├── types/
│   └── styles/
├── public/
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
├── Dockerfile
└── .env.example
```

---

## 5. Coding Standards

**General**
- Chhote, single-responsibility functions. Ek function = ek kaam.
- Naam clear rakho; `data`, `temp`, `x` jaise naam mat.
- No hardcoded secrets — sab `.env` se.
- Har external input validate karo (Pydantic / Zod).

**Python**
- Style: PEP8, formatter = **Black**, linter = **Ruff**, imports = isort.
- Type hints **compulsory** on functions.
- Docstrings for services and public functions.
- Async everywhere for I/O (DB, HTTP, Redis).

**TypeScript/React**
- `strict: true` in tsconfig. `any` avoid karo.
- Functional components + hooks only.
- Formatter = Prettier, linter = ESLint.
- Component file = PascalCase (`TicketCard.tsx`); hooks = `useX.ts`.
- API calls sirf `src/api/` layer se; component me raw axios nahi.

---

## 6. API Conventions

- Base path: **`/api/v1`**. Version badhega to `/api/v2`.
- REST resource naming: **plural nouns** — `/tickets`, `/users`, `/customers`.
- HTTP methods: GET (read), POST (create), PUT/PATCH (update), DELETE (remove).
- **Standard response shape:**
  ```json
  { "success": true, "data": { }, "message": "OK" }
  ```
  Error:
  ```json
  { "success": false, "error": { "code": "TICKET_NOT_FOUND", "message": "..." } }
  ```
- Status codes: 200 ok, 201 created, 204 no-content, 400 bad-req, 401 unauth,
  403 forbidden, 404 not-found, 409 conflict, 422 validation, 500 server.
- Pagination: `?page=1&limit=20`, response me `meta: {page, limit, total}`.
- Filtering/sorting: `?status=open&sort=-created_at`.
- Auth: `Authorization: Bearer <access_token>`.
- Har endpoint OpenAPI/Swagger me auto-documented (FastAPI free me deta hai).

---

## 7. Database Conventions

- Table names: **plural, snake_case** — `users`, `tickets`, `ticket_comments`.
- Primary key: `id` (UUID preferred, ya BigInt) — project bhar ek jaisa.
- Har table me: `created_at`, `updated_at` (timestamptz, default now).
- Soft delete jahan zaroori: `deleted_at` (nullable). Hard delete sirf jahan safe.
- Foreign keys: `<singular>_id` — `user_id`, `ticket_id`.
- Indexes: har FK par, aur jis column par filter/sort hota hai (`status`, `created_at`).
- Constraints: NOT NULL jahan chahiye, UNIQUE (e.g. `users.email`), CHECK for enums.
- Enums: DB enum ya string + CHECK — dono me se ek convention pick karke stick karo.
- **Har schema change = ek Alembic migration.** Manual DB edit kabhi nahi.
- pgvector: embeddings column `vector(768)` (model dimension ke hisaab se).

---

## 8. Git Conventions

**Branch strategy**
- `main` — hamesha deployable, protected.
- `develop` — integration branch (optional agar team chhoti hai).
- Feature branches: `feature/<phase>-<short-name>` e.g. `feature/05-authentication`.
- Fix branches: `fix/<short-name>`. Hotfix: `hotfix/<short-name>`.
- PR se merge; direct `main` par push nahi (jab team ho).

**Commit message format (Conventional Commits)**
```
<type>(<scope>): <short summary>

<optional body — kyun/kya>
```
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`.
Examples:
- `feat(auth): add JWT login and refresh token`
- `feat(tickets): create ticket CRUD endpoints`
- `docs(readme): add setup instructions`

**Suggested milestone commit history** (recruiter ko organic growth dikhta hai):
```
chore: initial project setup
feat(backend): initialize FastAPI app
feat(frontend): initialize React app
feat(auth): authentication completed
feat(auth): RBAC added
feat(customer): customer module added
feat(ticket): ticket module added
feat(kb): knowledge base added
feat(ai): ollama integration
feat(ai): RAG completed
feat(dashboard): analytics dashboard
chore(docker): docker support
ci: github actions pipeline added
chore: production ready — release v1.0
```

---

## 9. Testing Checklist (har phase ke end me)

- [ ] Unit tests for services/business logic
- [ ] API tests (happy path + error path) via pytest + httpx
- [ ] Auth/permission tests (galat role → 403)
- [ ] Validation tests (bad input → 422)
- [ ] Frontend: key components render + user flow (Vitest + React Testing Library)
- [ ] Manual smoke test: feature actually chal raha hai
- [ ] No console errors / no server 500 in normal flow

---

## 10. Deployment Checklist

- [ ] All services Dockerized (backend, frontend, db, redis)
- [ ] `docker-compose up` se pura stack chalta hai
- [ ] Env vars documented in `.env.example`, secrets NOT committed
- [ ] DB migrations run automatically / documented
- [ ] Health check endpoint `/health`
- [ ] Nginx reverse proxy + HTTPS (prod)
- [ ] Logs structured, error monitoring set
- [ ] Backup strategy for Postgres

---

## 11. README Checklist

- [ ] Project title + one-line description + screenshot/GIF
- [ ] Features list
- [ ] Tech stack badges
- [ ] Architecture diagram
- [ ] Prerequisites
- [ ] Setup (local) — step by step
- [ ] Setup (docker) — `docker-compose up`
- [ ] Environment variables table
- [ ] API docs link (Swagger)
- [ ] Folder structure
- [ ] Roadmap / phases
- [ ] Contributing + License

---

## 12. Security Checklist

- [ ] Passwords hashed (bcrypt/argon2), never plain
- [ ] JWT: short-lived access + refresh rotation; secrets in env
- [ ] RBAC enforced on every protected endpoint (server-side, not just UI)
- [ ] Input validation everywhere (Pydantic/Zod)
- [ ] SQL injection safe (ORM, no string-built queries)
- [ ] CORS locked to known origins
- [ ] Rate limiting on auth endpoints
- [ ] No secrets in git; `.env` in `.gitignore`
- [ ] HTTPS in production
- [ ] File upload validation (type/size) if used

---

## 13. Standard Phase Template

**Har phase ka output isi structure me hoga:**

```
1. Goal            — is phase me kya achieve karna hai (1-2 line)
2. Requirements    — kya-kya chahiye (libs, prior phases)
3. Folder Structure— naye/badle hue files ka tree
4. Implementation  — actual code / steps
5. Best Practices  — is phase me kin baaton ka dhyaan
6. Possible Errors — common galtiyan + fix
7. Testing         — kya test karna hai (checklist se)
8. Git Commit      — exact commit message
9. README Update   — README me kya add karna
10. Next Phase     — aage kya
```

---

## 14. Full 20-Phase Roadmap + Ready Prompts

> Har phase ke liye AI ko diya jaane wala prompt neeche `PROMPT:` me hai.
> Prefix hamesha: *"Tum Senior Software Architect / Tech Lead ho. PROJECT_MASTER_GUIDE.md
> follow karo. Sirf is phase ka kaam karo."*

### Phase 0 — Requirement Analysis (no code)
Requirement analysis, feature list, user roles, user flows, final scope.
`PROMPT:` "Phase 0 karo. Sirf requirement analysis — features, user roles, complete
user flows (customer/agent/admin), aur final scope define karo. Code mat likho.
Output `docs/01_Project_Overview.md` me."

### Phase 1 — System Architecture + Database Design (no code)
`PROMPT:` "Phase 1 karo. System architecture, high-level diagram, database ER design
(tables, relations, indexes, constraints), API list, folder structure, tech stack
finalize. Code mat likho. Output `docs/02_System_Architecture.md`, `03_Database.md`,
`04_API_Design.md` me. Explain karo production companies kaise design karti hain."

### Phase 2 — Repo, README, Docker skeleton, env, initial commit
`PROMPT:` "Phase 2 karo. GitHub repo structure, README (checklist follow), branch
strategy, docker-compose skeleton, `.env.example`, `.gitignore`. Initial commit ready
karo. Abhi feature code nahi."

### Phase 3 — Backend Setup (FastAPI, SQLAlchemy, Alembic, Postgres, Redis, JWT base)
`PROMPT:` "Phase 3 karo. Backend skeleton — FastAPI app factory, config, database
(async SQLAlchemy), Alembic init, Redis connection, JWT utilities, `/health` endpoint.
Ek dummy model + migration se prove karo setup chalta hai."

### Phase 4 — Frontend Setup (React, TS, Tailwind, routing, state, base UI)
`PROMPT:` "Phase 4 karo. Frontend skeleton — Vite + React + TS + Tailwind, routing,
axios client with interceptors, base layout, state setup. Ek sample page se prove karo."

### Phase 5 — Authentication (Login, Register, Refresh, Forgot password, RBAC, Profile)
`PROMPT:` "Phase 5 karo. Full auth — register, login, refresh token, forgot/reset
password, RBAC (Admin/Agent/Customer), user profile. Backend + frontend dono. Tests bhi."

### Phase 6 — Customer Module
`PROMPT:` "Phase 6 karo. Customer module — CRUD, list/search/pagination, customer detail.
Backend + frontend + tests."

### Phase 7 — Ticket Module
`PROMPT:` "Phase 7 karo. Ticket module — create/assign/status/priority/comments,
filters, list, detail. Backend + frontend + tests."

### Phase 8 — Live Chat
`PROMPT:` "Phase 8 karo. Live chat — WebSocket (FastAPI), Redis pub-sub, agent↔customer
messaging, chat history, online status. Frontend chat UI. Tests."

### Phase 9 — Knowledge Base
`PROMPT:` "Phase 9 karo. Knowledge base — articles CRUD, categories, search. Ye AI RAG
ka source banega. Backend + frontend + tests."

### Phase 10 — AI Module (Ollama, Embeddings, RAG, Prompts, Memory, Streaming)
`PROMPT:` "Phase 10 karo. AI module — AIProvider abstraction (Ollama default), embeddings
of KB articles into pgvector, RAG pipeline, prompt templates, conversation memory,
streaming responses. Tests for retrieval + generation."

### Phase 11 — Dashboard
`PROMPT:` "Phase 11 karo. Role-based dashboard — key metrics cards, recent tickets/chats.
Frontend + supporting endpoints."

### Phase 12 — Analytics
`PROMPT:` "Phase 12 karo. Analytics — tickets over time, resolution time, agent
performance, AI usage. Charts. Backend aggregation endpoints + frontend."

### Phase 13 — Notifications
`PROMPT:` "Phase 13 karo. Notifications — in-app (WebSocket) + email. Events: ticket
assigned, new reply, chat message. Preferences."

### Phase 14 — Testing
`PROMPT:` "Phase 14 karo. Testing pass — coverage badhao, integration tests, e2e for
critical flows, fix flaky tests. Coverage report."

### Phase 15 — Docker
`PROMPT:` "Phase 15 karo. Full dockerization — backend, frontend, postgres+pgvector,
redis, nginx. docker-compose for dev + prod. `docker-compose up` sab chale."

### Phase 16 — CI/CD
`PROMPT:` "Phase 16 karo. GitHub Actions — lint, test, build on PR; build+push images on
main. Branch protection. Status badges."

### Phase 17 — Deployment
`PROMPT:` "Phase 17 karo. Deployment guide + config — VPS/cloud, nginx, HTTPS, env,
migrations, healthchecks, backups."

### Phase 18 — Documentation
`PROMPT:` "Phase 18 karo. Complete docs/ — sab 12 files bharo, diagrams, API docs,
architecture, deployment. Polished."

### Phase 19 — Screenshots
`PROMPT:` "Phase 19 karo. Screenshots/GIFs of key features for README. Ek demo script."

### Phase 20 — Release v1.0
`PROMPT:` "Phase 20 karo. Final review vs checklists, version bump, CHANGELOG,
`12_Release_Notes.md`, git tag `v1.0`, GitHub release."

---

## 15. docs/ Structure

```
docs/
├── 01_Project_Overview.md
├── 02_System_Architecture.md
├── 03_Database.md
├── 04_API_Design.md
├── 05_Backend.md
├── 06_Frontend.md
├── 07_AI_Module.md
├── 08_RAG.md
├── 09_Deployment.md
├── 10_Testing.md
├── 11_Security.md
└── 12_Release_Notes.md
```

---

## 16. Definition of Done (DoD) — ek phase "done" kab?

Ek phase tabhi done maana jaayega jab:
- [ ] Feature kaam kar raha hai (manual smoke test pass)
- [ ] Tests likhe aur pass hue
- [ ] Coding standards + conventions follow hue
- [ ] Relevant `docs/` file update hui
- [ ] README update (agar zaroori)
- [ ] Ek clean commit with proper message
- [ ] Push to GitHub
- [ ] `Next Phase` note likha

---

**Golden Rule:** *Ek phase → ek focus → test → commit → push → next.
Kabhi "pura project ek saath" nahi.*
