# 01 — Project Overview

> **Phase 0 — Requirement Analysis.** Yahan sirf _kya banana hai_ define hota hai —
> koi code nahi. Ye document poore project ka base hai.

---

## 1. Vision

**Helpdesk AI** ek AI-powered customer support platform hai jahan:
- Customers apne issues **tickets** ke through raise karte hain ya **live chat** karte hain.
- Support **agents** in tickets/chats ko manage karte hain.
- Ek **AI assistant** (RAG-based) knowledge base se turant, accurate jawaab deta hai —
  aur agents ko reply suggest karta hai.
- **Admin** poore system, users, roles aur analytics ko control karta hai.

**Goal:** support team ka response time kam karna, repetitive sawaalon ko AI se auto-handle
karna, aur ek hi jagah se pura support operation chalana.

---

## 2. Features

### 2.1 Core Features (v1.0)

**Authentication & Users**
- Register / Login / Logout
- JWT access + refresh token
- Forgot / Reset password
- Role-Based Access Control (RBAC)
- User profile (view/edit, avatar, password change)

**Customer Management**
- Customer create / view / edit / delete
- Customer list with search, filter, pagination
- Customer detail page (profile + uska ticket history)

**Ticket Management**
- Ticket create (customer ya agent dwara)
- Fields: subject, description, status, priority, category, assignee
- Status flow: `open → in_progress → resolved → closed`
- Priority: `low / medium / high / urgent`
- Assign / reassign ticket to agent
- Ticket comments / replies (thread)
- Attachments (optional)
- Filters: status, priority, assignee, date; sort; pagination

**Live Chat**
- Real-time agent ↔ customer chat (WebSocket)
- Chat history persist
- Online/offline status
- Chat ko ticket me convert karna (optional)

**Knowledge Base (KB)**
- Articles: create / edit / delete / publish
- Categories & tags
- Search
- Public-facing article view (customer padh sake)
- Ye KB hi AI ke RAG ka data source hai

**AI Assistant**
- Customer question → AI answer (KB se RAG)
- Agent assist: reply suggestion
- Streaming responses (typing effect)
- Conversation memory (context yaad rahe)
- "AI ko nahi pata" → gracefully agent ko escalate

**Dashboard**
- Role-based dashboard (Admin/Agent alag)
- Key metric cards, recent activity

**Analytics**
- Tickets over time, by status/priority
- Average resolution time
- Agent performance
- AI usage & deflection rate

**Notifications**
- In-app (real-time) + email
- Events: ticket assigned, new reply, new chat message

### 2.2 Non-Functional Requirements
- **Performance:** common API < 300ms; AI streaming turant shuru ho.
- **Security:** hashed passwords, RBAC server-side, input validation, HTTPS.
- **Scalability:** stateless backend, Redis for sessions/pub-sub, Docker.
- **Reliability:** health checks, error logging, DB backups.
- **Usability:** clean responsive UI, clear error messages.
- **Maintainability:** layered code, conventions (see MASTER_GUIDE).

---

## 3. User Roles & Permissions

| Capability | Admin | Agent | Customer |
|------------|:-----:|:-----:|:--------:|
| Login / Profile | ✅ | ✅ | ✅ |
| Manage users & roles | ✅ | ❌ | ❌ |
| System settings | ✅ | ❌ | ❌ |
| View all tickets | ✅ | ✅ | ❌ (sirf apne) |
| Create ticket | ✅ | ✅ | ✅ |
| Assign / reassign ticket | ✅ | ✅ | ❌ |
| Comment on ticket | ✅ | ✅ | ✅ (apne) |
| Change ticket status | ✅ | ✅ | ❌ |
| Manage customers | ✅ | ✅ | ❌ |
| Live chat (agent side) | ✅ | ✅ | ❌ |
| Live chat (customer side) | ❌ | ❌ | ✅ |
| Manage Knowledge Base | ✅ | ✅ (edit) | ❌ |
| Read Knowledge Base | ✅ | ✅ | ✅ |
| Use AI assistant | ✅ | ✅ | ✅ |
| View analytics | ✅ | ✅ (limited) | ❌ |

**Roles summary**
- **Admin** — full control: users, roles, settings, sab tickets, analytics, KB.
- **Agent** — daily operations: tickets handle, chat, customers, KB edit, AI assist.
- **Customer** — self-service: apne tickets, chat, KB padhna, AI se poochhna.

---

## 4. User Flows

### 4.1 Customer — ticket raise karta hai
```
Register/Login → Dashboard → "New Ticket"
   → subject + description + category bharo → Submit
   → ticket "open" ban gaya → confirmation + notification
   → (optional) AI turant KB se suggested answer dikhata hai
   → agent reply kare to customer ko notification → thread me baat
   → issue solve → status "resolved" → customer confirm → "closed"
```

### 4.2 Customer — AI/KB se self-help
```
Login → Help/Chat → sawaal type karo
   → AI KB me search (RAG) → streaming answer + source articles
   → hal ho gaya → done
   → nahi hua → "Talk to agent" → live chat ya ticket ban jaata hai
```

### 4.3 Agent — ticket handle karta hai
```
Login → Agent Dashboard → assigned/open tickets list
   → ticket kholo → detail + customer history + AI suggested reply
   → reply likho (ya AI suggestion edit karo) → send
   → status update (in_progress/resolved)
   → zaroorat ho to dusre agent ko reassign
```

### 4.4 Agent — live chat
```
Login → Chat panel → incoming customer chat
   → real-time messages → AI suggestions side me
   → solve → chat close (optional: ticket me convert)
```

### 4.5 Admin — setup & monitor
```
Login → Admin Dashboard → users/roles manage
   → KB articles add/publish (AI ka knowledge badhao)
   → analytics dekho (volume, resolution time, AI deflection)
   → settings configure
```

---

## 5. Final Scope

### ✅ In Scope (v1.0)
- Auth + RBAC (Admin/Agent/Customer)
- Customer module
- Ticket module (full lifecycle + comments)
- Live chat (WebSocket)
- Knowledge Base
- AI assistant (Ollama + embeddings + RAG + streaming + memory)
- Dashboard + Analytics
- Notifications (in-app + email)
- Docker + CI/CD + Deployment + Docs + Tests

### ❌ Out of Scope (v1.0 — future)
- Billing / payments / subscriptions
- Multi-language (i18n) UI
- Native mobile app
- Voice / telephony / call center
- Third-party integrations (Slack, WhatsApp, etc.)
- Multi-tenant / white-label
- SLA automation & advanced workflow rules

### Assumptions
- Single organization (multi-tenant nahi).
- Email bhejne ke liye ek SMTP available hai.
- Ollama chalane ke liye machine me enough resources hain (ya remote Ollama).

### Success Criteria (v1.0 "done")
- Teeno roles apna full flow kar paayein.
- AI KB se relevant answer + source de.
- `docker-compose up` se pura stack chale.
- Core flows tested; CI green; deployed + documented.

---

## 6. Next Phase
**Phase 1 — System Architecture + Database Design + API Planning.**
Output: `02_System_Architecture.md`, `03_Database.md`, `04_API_Design.md`.
