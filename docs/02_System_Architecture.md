# 02 — System Architecture

> **Phase 1.** System ka high-level design. Code nahi — sirf structure aur decisions.

---

## 1. Architecture Style

**Modular Monolith** (v1.0) — ek FastAPI backend jisme feature modules alag-alag hain
(auth, customer, ticket, chat, kb, ai). Microservices nahi, kyunki:
- Team chhoti, tezi se ship karna hai.
- Ek deployable unit = simple ops.
- Modules clean-separated hain, to future me service me todna aasan.

Frontend alag SPA (React) hai jo REST + WebSocket se backend se baat karta hai.

---

## 2. High-Level Diagram

```
                    ┌──────────────────────────────┐
                    │           Browser              │
                    │   React + TS + Tailwind SPA    │
                    └───────┬───────────────┬────────┘
                    REST/JSON│               │WebSocket (chat, notifications)
                             ▼               ▼
                    ┌──────────────────────────────┐
                    │            Nginx               │  (prod: reverse proxy + HTTPS)
                    └───────────────┬────────────────┘
                                    ▼
                    ┌──────────────────────────────┐
                    │           FastAPI              │
                    │  ┌────────────────────────┐    │
                    │  │ API Routers (/api/v1)  │    │
                    │  ├────────────────────────┤    │
                    │  │ Services (business)    │    │
                    │  ├────────────────────────┤    │
                    │  │ Repositories (DB I/O)  │    │
                    │  └────────────────────────┘    │
                    │  Modules: auth, customer,      │
                    │  ticket, chat, kb, ai          │
                    └───┬─────────┬─────────┬─────────┘
                        ▼         ▼         ▼
                ┌───────────┐ ┌───────┐ ┌──────────────┐
                │PostgreSQL │ │ Redis │ │  AI Layer     │
                │+ pgvector │ │cache/ │ │  Ollama LLM   │
                │           │ │pubsub │ │  + embeddings │
                └───────────┘ └───────┘ └──────────────┘
```

---

## 3. Components

| Component | Zimmedari |
|-----------|-----------|
| **React SPA** | UI, routing, state, API calls, WebSocket client |
| **Nginx** | Reverse proxy, HTTPS, static serve, load balancing (prod) |
| **FastAPI** | REST API, WebSocket, auth, business logic |
| **PostgreSQL** | Primary data store (users, tickets, KB, etc.) |
| **pgvector** | KB article embeddings — RAG ka vector search |
| **Redis** | Cache, session/refresh-token store, WebSocket pub-sub, rate limit |
| **AI Layer** | Ollama (LLM + embeddings), RAG pipeline, prompt templates |

---

## 4. Layering Rule (backend)

```
HTTP Request
   ▼
Router      → request parse, auth check, call service, return response
   ▼
Service     → business logic, rules, orchestration (multiple repos/AI)
   ▼
Repository  → sirf DB access (SQLAlchemy queries)
   ▼
Model / DB
```

**Rules:**
- Router me business logic **nahi**.
- Service SQLAlchemy query **directly nahi** karega — repository se.
- Repository HTTP/Pydantic ke baare me kuch **nahi** jaanega.
- AI calls service layer se, `ai/` module ke through.

---

## 5. Key Data Flows

### 5.1 REST request (e.g. create ticket)
```
React → POST /api/v1/tickets (Bearer token)
  → Router: validate + get_current_user + RBAC
  → Service: business rules (assign, defaults)
  → Repository: INSERT
  → response {success, data}
  → Notification event (agent ko)
```

### 5.2 AI answer (RAG, streaming)
```
React → POST /api/v1/ai/ask (question)
  → Service: embed question → pgvector search (top-k KB chunks)
  → build prompt (template + context + memory)
  → Ollama generate (stream)
  → tokens stream back to React (SSE/WebSocket)
  → store conversation turn (memory)
```

### 5.3 Live chat (WebSocket + Redis pub-sub)
```
Customer WS ─┐                       ┌─ Agent WS
             ├─ FastAPI WS manager ──┤
             │   publish/subscribe   │
             └────── Redis pubsub ───┘   (multi-worker ke liye)
messages DB me persist hote hain (chat history)
```

---

## 6. Authentication Flow (high-level)

```
Login → verify password → issue access(15m) + refresh(7d)
access token har request me (Bearer)
access expire → /auth/refresh (refresh token) → naya access
refresh token Redis me store (rotation + revoke support)
logout → refresh token Redis se delete
```

---

## 7. Environments

| Env | Purpose | Notes |
|-----|---------|-------|
| **local** | dev | docker-compose, hot reload |
| **staging** | testing | prod-like, sample data |
| **production** | live | Nginx+HTTPS, backups, monitoring |

---

## 8. Tech Stack Justification (short)

- **FastAPI** — async, fast, auto OpenAPI docs, Pydantic validation.
- **PostgreSQL + pgvector** — reliable relational DB + vector search ek hi jagah (kam moving parts).
- **Redis** — cache + pub-sub + token store, ek tool se kai kaam.
- **React + TS** — mature ecosystem, type-safety.
- **Ollama** — local, free, private AI; provider-abstraction se Claude API par switch possible.
- **Docker** — consistent env, aasan deploy.

---

## 9. Next
`03_Database.md` (ER + tables) aur `04_API_Design.md` (endpoints).
