<h1 align="center">🎧 Helpdesk AI</h1>

<p align="center">
  <b>Production-ready AI-powered customer support platform</b><br/>
  React · FastAPI · PostgreSQL · Redis · Ollama · RAG
</p>

---

## 📖 Overview

Helpdesk AI ek modern customer support platform hai jahan customers tickets/live-chat ke
through help maangte hain, agents unhe manage karte hain, aur ek **RAG-based AI assistant**
knowledge base se turant, accurate jawaab deta hai.

> 🏗️ Ye project ek strict **phase-by-phase** roadmap follow karke banaya ja raha hai.
> Full plan: [`PROJECT_MASTER_GUIDE.md`](./PROJECT_MASTER_GUIDE.md) · Docs: [`docs/`](./docs)

---

## ✨ Features

- 🔐 **Auth & RBAC** — JWT (access+refresh), roles: Admin / Agent / Customer
- 👥 **Customer Management** — profiles, history, search
- 🎫 **Ticket System** — lifecycle, priority, assignment, comments
- 💬 **Live Chat** — real-time (WebSocket) agent ↔ customer
- 📚 **Knowledge Base** — articles, categories, search (AI ka data source)
- 🤖 **AI Assistant** — Ollama + embeddings + **RAG** + streaming + memory
- 📊 **Dashboard & Analytics** — metrics, resolution time, AI deflection
- 🔔 **Notifications** — in-app (real-time) + email

---

## 🧱 Tech Stack

| Layer | Tech |
|-------|------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, TanStack Query |
| **Backend** | FastAPI, SQLAlchemy (async), Alembic, Pydantic v2 |
| **Database** | PostgreSQL 16 + pgvector |
| **Cache/Realtime** | Redis 7 |
| **AI** | Ollama (LLM + embeddings), RAG |
| **DevOps** | Docker, docker-compose, GitHub Actions, Nginx |

---

## 🗺️ Architecture

```
React SPA ──REST/WS──► Nginx ──► FastAPI ──► PostgreSQL + pgvector
                                     │  ├────► Redis (cache / pub-sub)
                                     │  └────► Ollama (AI + RAG)
```
Detail: [`docs/02_System_Architecture.md`](./docs/02_System_Architecture.md)

---

## 🚀 Getting Started

> ⚠️ Project abhi active development me hai (phase-by-phase). Setup steps har phase ke
> saath complete hote jaayenge.

### Prerequisites
- Docker & docker-compose
- (local dev) Python 3.11+, Node 20+
- Ollama installed (AI phase ke liye)

### Quick start (Docker)
```bash
git clone https://github.com/sanket801036/helpdesk-ai.git
cd helpdesk-ai
cp .env.example .env          # values bharo
docker-compose up --build
```
- Frontend: http://localhost:5173
- Backend API + docs: http://localhost:8000/api/v1/docs

---

## 📁 Project Structure

```
helpdesk-ai/
├── PROJECT_MASTER_GUIDE.md   # complete roadmap + conventions
├── docs/                     # design & phase documentation (01..12)
├── backend/                  # FastAPI app        (Phase 3+)
├── frontend/                 # React app          (Phase 4+)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🧭 Roadmap (20 Phases)

`Phase 0` Requirements → `1` Architecture/DB → `2` Repo Setup → `3` Backend →
`4` Frontend → `5` Auth → `6` Customers → `7` Tickets → `8` Chat → `9` KB →
`10` AI/RAG → `11` Dashboard → `12` Analytics → `13` Notifications → `14` Testing →
`15` Docker → `16` CI/CD → `17` Deploy → `18` Docs → `19` Screenshots → `20` Release v1.0

Full detail: [`PROJECT_MASTER_GUIDE.md`](./PROJECT_MASTER_GUIDE.md)

---

## 🤝 Contributing

Branch strategy aur commit conventions: `PROJECT_MASTER_GUIDE.md §8`.
Har PR ek phase/feature ke liye. Commits = Conventional Commits.

## 📄 License

MIT (TBD)
