# 04 — API Design

> **Phase 1.** REST + WebSocket endpoints. Conventions: `MASTER_GUIDE §6`.
> Base path: `/api/v1`. Auth: `Authorization: Bearer <access_token>`.

---

## 1. Conventions Recap
- Resources: plural nouns (`/tickets`, `/users`).
- Success: `{ "success": true, "data": ..., "message": "OK" }`
- Error: `{ "success": false, "error": { "code": "...", "message": "..." } }`
- Pagination: `?page=1&limit=20` → `meta: {page, limit, total}`
- Filter/sort: `?status=open&sort=-created_at`

---

## 2. Auth Endpoints

| Method | Path | Access | Desc |
|--------|------|--------|------|
| POST | `/auth/register` | public | naya user (customer default) |
| POST | `/auth/login` | public | email+password → access+refresh |
| POST | `/auth/refresh` | public (refresh token) | naya access token |
| POST | `/auth/logout` | auth | refresh token revoke |
| POST | `/auth/forgot-password` | public | reset email bhejo |
| POST | `/auth/reset-password` | public (token) | naya password set |
| GET | `/auth/me` | auth | current user info |

---

## 3. User Endpoints

| Method | Path | Access | Desc |
|--------|------|--------|------|
| GET | `/users` | admin | list (filter role, search, paginate) |
| POST | `/users` | admin | create user (role assign) |
| GET | `/users/{id}` | admin/self | detail |
| PATCH | `/users/{id}` | admin/self | update |
| DELETE | `/users/{id}` | admin | deactivate/delete |
| PATCH | `/users/me/profile` | auth | apna profile |
| PATCH | `/users/me/password` | auth | password change |

---

## 4. Customer Endpoints

| Method | Path | Access | Desc |
|--------|------|--------|------|
| GET | `/customers` | admin/agent | list + search + paginate |
| POST | `/customers` | admin/agent | create |
| GET | `/customers/{id}` | admin/agent | detail + ticket history |
| PATCH | `/customers/{id}` | admin/agent | update |
| DELETE | `/customers/{id}` | admin | delete |

---

## 5. Ticket Endpoints

| Method | Path | Access | Desc |
|--------|------|--------|------|
| GET | `/tickets` | role-scoped | list (customer→apne; agent/admin→sab) filters: status, priority, assignee |
| POST | `/tickets` | auth | create ticket |
| GET | `/tickets/{id}` | role-scoped | detail |
| PATCH | `/tickets/{id}` | agent/admin | update (status, priority, category) |
| PATCH | `/tickets/{id}/assign` | agent/admin | assign/reassign |
| DELETE | `/tickets/{id}` | admin | delete |
| GET | `/tickets/{id}/comments` | role-scoped | thread |
| POST | `/tickets/{id}/comments` | auth | add comment/reply |

---

## 6. Knowledge Base Endpoints

| Method | Path | Access | Desc |
|--------|------|--------|------|
| GET | `/kb/articles` | auth | list published (agent/admin→drafts bhi) |
| POST | `/kb/articles` | agent/admin | create |
| GET | `/kb/articles/{id}` | auth | detail |
| PATCH | `/kb/articles/{id}` | agent/admin | update |
| DELETE | `/kb/articles/{id}` | admin | delete |
| POST | `/kb/articles/{id}/publish` | agent/admin | publish (triggers embedding) |
| GET | `/kb/search?q=...` | auth | text search |

---

## 7. AI Endpoints

| Method | Path | Access | Desc |
|--------|------|--------|------|
| POST | `/ai/ask` | auth | question → RAG answer (streaming) |
| POST | `/ai/suggest-reply` | agent/admin | ticket/chat ke liye reply suggestion |
| GET | `/ai/conversations` | auth | user ki AI conversations |
| GET | `/ai/conversations/{id}` | auth | ek conversation ke messages |
| POST | `/ai/reindex` | admin | KB embeddings rebuild |

> Streaming: `/ai/ask` SSE (`text/event-stream`) ya WebSocket se tokens bhejta hai.

---

## 8. Chat (WebSocket)

| Type | Path | Desc |
|------|------|------|
| WS | `/ws/chat/{session_id}` | live chat channel (customer/agent) |
| REST | `GET /chat/sessions` | agent: active sessions |
| REST | `POST /chat/sessions` | customer: naya chat shuru |
| REST | `GET /chat/sessions/{id}/messages` | history |
| REST | `POST /chat/sessions/{id}/close` | close session |

**WS message shape:**
```json
{ "type": "message", "body": "...", "sender_type": "customer" }
```

---

## 9. Notifications

| Method | Path | Access | Desc |
|--------|------|--------|------|
| GET | `/notifications` | auth | list (unread filter) |
| PATCH | `/notifications/{id}/read` | auth | mark read |
| PATCH | `/notifications/read-all` | auth | sab read |
| WS | `/ws/notifications` | auth | real-time push |

---

## 10. Analytics

| Method | Path | Access | Desc |
|--------|------|--------|------|
| GET | `/analytics/overview` | admin/agent | key metrics |
| GET | `/analytics/tickets` | admin/agent | volume over time, by status/priority |
| GET | `/analytics/agents` | admin | agent performance |
| GET | `/analytics/ai` | admin | AI usage & deflection |

---

## 11. System

| Method | Path | Desc |
|--------|------|------|
| GET | `/health` | health check (db, redis, ollama) |
| GET | `/api/v1/docs` | Swagger UI (FastAPI auto) |

---

## 12. Common Error Codes
| code | HTTP | meaning |
|------|------|---------|
| `VALIDATION_ERROR` | 422 | bad input |
| `UNAUTHORIZED` | 401 | token missing/invalid |
| `FORBIDDEN` | 403 | role allowed nahi |
| `NOT_FOUND` | 404 | resource nahi |
| `CONFLICT` | 409 | duplicate (e.g. email) |
| `RATE_LIMITED` | 429 | too many requests |
| `SERVER_ERROR` | 500 | internal |

---

## 13. Next
**Phase 2 — Repo setup, README, Docker skeleton, `.env.example`, initial commit.**
