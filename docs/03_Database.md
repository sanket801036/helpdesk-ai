# 03 — Database Design

> **Phase 1.** PostgreSQL schema design. Conventions: `MASTER_GUIDE §7`.
> Sab tables me `id` (UUID), `created_at`, `updated_at`. Snake_case, plural table names.

---

## 1. ER Diagram (high-level)

```
                 ┌──────────┐
                 │  users   │
                 └────┬─────┘
        ┌─────────────┼───────────────┬───────────────┐
        │ (assignee)  │ (author)      │ (agent)       │
        ▼             ▼               ▼               │
  ┌──────────┐  ┌──────────────┐ ┌──────────────┐    │
  │ tickets  │  │ kb_articles  │ │ chat_sessions│    │
  └────┬─────┘  └──────┬───────┘ └──────┬───────┘    │
       │               │                │            │
       ▼               ▼                ▼            │
┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│ticket_comments│ │kb_embeddings │ │ chat_messages│  │
└──────────────┘ └──────────────┘ └──────────────┘  │
                                                      │
  ┌──────────┐        ┌───────────────┐   ┌──────────▼────┐
  │customers │───────▶│    tickets    │   │ notifications │
  └──────────┘        └───────────────┘   └───────────────┘
                      ┌───────────────────────┐
                      │ ai_conversations /     │
                      │ ai_messages (memory)   │
                      └───────────────────────┘
```

---

## 2. Tables

### users
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| email | varchar UNIQUE NOT NULL | login |
| password_hash | varchar NOT NULL | bcrypt/argon2 |
| full_name | varchar | |
| role | enum(`admin`,`agent`,`customer`) NOT NULL | RBAC |
| is_active | bool default true | |
| avatar_url | varchar NULL | |
| created_at / updated_at | timestamptz | |

### customers
> Customer = jis end-user ka support ho raha hai. (Ho sakta hai ek `user` bhi ho agar wo login karta hai; ya sirf record.)

| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| user_id | UUID FK→users NULL | agar login-able customer |
| name | varchar NOT NULL | |
| email | varchar | |
| phone | varchar NULL | |
| company | varchar NULL | |
| notes | text NULL | |
| created_at / updated_at | timestamptz | |

### tickets
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| ticket_number | serial/int UNIQUE | human-friendly (#1024) |
| subject | varchar NOT NULL | |
| description | text | |
| status | enum(`open`,`in_progress`,`resolved`,`closed`) default `open` | |
| priority | enum(`low`,`medium`,`high`,`urgent`) default `medium` | |
| category | varchar NULL | |
| customer_id | UUID FK→customers | |
| assignee_id | UUID FK→users NULL | agent |
| created_by | UUID FK→users | |
| resolved_at | timestamptz NULL | |
| created_at / updated_at | timestamptz | |

### ticket_comments
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| ticket_id | UUID FK→tickets | |
| author_id | UUID FK→users | |
| body | text NOT NULL | |
| is_internal | bool default false | agent-only note |
| created_at | timestamptz | |

### kb_articles
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| title | varchar NOT NULL | |
| slug | varchar UNIQUE | |
| content | text | markdown |
| category | varchar NULL | |
| tags | varchar[] / text NULL | |
| status | enum(`draft`,`published`) default `draft` | |
| author_id | UUID FK→users | |
| created_at / updated_at | timestamptz | |

### kb_embeddings  (pgvector)
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| article_id | UUID FK→kb_articles | |
| chunk_index | int | article ka kaunsa chunk |
| chunk_text | text | |
| embedding | vector(768) | model dimension ke hisaab se |
| created_at | timestamptz | |

### chat_sessions
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| customer_id | UUID FK→customers | |
| agent_id | UUID FK→users NULL | |
| status | enum(`active`,`closed`) default `active` | |
| started_at / closed_at | timestamptz | |

### chat_messages
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| session_id | UUID FK→chat_sessions | |
| sender_type | enum(`customer`,`agent`,`ai`) | |
| sender_id | UUID NULL | |
| body | text NOT NULL | |
| created_at | timestamptz | |

### ai_conversations / ai_messages  (AI memory)
**ai_conversations:** id, user_id FK, title, created_at.
**ai_messages:** id, conversation_id FK, role(`user`/`assistant`/`system`), content, created_at.

### notifications
| column | type | notes |
|--------|------|-------|
| id | UUID PK | |
| user_id | UUID FK→users | recipient |
| type | varchar | e.g. `ticket_assigned` |
| title / body | varchar/text | |
| data | jsonb NULL | extra payload |
| is_read | bool default false | |
| created_at | timestamptz | |

---

## 3. Relations (summary)
- `users` 1─N `tickets` (assignee), 1─N `tickets` (created_by)
- `customers` 1─N `tickets`
- `tickets` 1─N `ticket_comments`
- `users` 1─N `kb_articles` (author)
- `kb_articles` 1─N `kb_embeddings`
- `customers` 1─N `chat_sessions`; `chat_sessions` 1─N `chat_messages`
- `users` 1─N `ai_conversations`; `ai_conversations` 1─N `ai_messages`
- `users` 1─N `notifications`

---

## 4. Indexes
- `users.email` (UNIQUE)
- `tickets.status`, `tickets.priority`, `tickets.assignee_id`, `tickets.customer_id`, `tickets.created_at`
- `ticket_comments.ticket_id`
- `kb_articles.slug` (UNIQUE), `kb_articles.status`
- `kb_embeddings.article_id`; vector index (ivfflat/hnsw) on `embedding`
- `chat_messages.session_id`
- `notifications.user_id`, `notifications.is_read`

---

## 5. Constraints
- NOT NULL on required cols; UNIQUE on `email`, `slug`, `ticket_number`.
- FK constraints with sensible ON DELETE (e.g. comments cascade with ticket).
- Enums via DB enum ya CHECK (project bhar consistent).
- `resolved_at` set jab status `resolved` ho.

---

## 6. Migration Plan
- **Alembic** se har change ek migration.
- Naming: `alembic revision -m "create users table"`.
- pgvector extension: pehli migration me `CREATE EXTENSION IF NOT EXISTS vector;`
- Order: users → customers → tickets → ticket_comments → kb_articles →
  kb_embeddings → chat_sessions → chat_messages → ai_* → notifications.
- Seed script: ek default admin user (dev ke liye).

---

## 7. Next
`04_API_Design.md`.
