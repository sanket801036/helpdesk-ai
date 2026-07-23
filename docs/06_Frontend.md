# 06 — Frontend

> **Phase 4 — Frontend Setup.** React + TS + Vite + Tailwind skeleton.
> Ek Home page backend `/health` ko call karke connection status dikhata hai.

---

## 1. Run

**Docker (recommended)** — root se sab ek saath:
```bash
docker-compose up --build
```
- Frontend: http://localhost:5173
- Backend:  http://localhost:8000/api/v1/docs

**Bina Docker (local dev):**
```bash
cd frontend
npm install
copy .env.example .env      # VITE_API_BASE_URL check karo
npm run dev                 # http://localhost:5173
```

---

## 2. Stack
| Cheez | Tech |
|-------|------|
| Framework | React 18 + TypeScript |
| Build | Vite |
| Styling | Tailwind CSS |
| Routing | React Router v6 |
| Server state | TanStack Query |
| HTTP | Axios (token interceptor ready) |

---

## 3. Folder Structure
```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── Dockerfile
├── .env.example
└── src/
    ├── main.tsx              # entry — Router + QueryClient providers
    ├── App.tsx               # routes
    ├── index.css             # tailwind directives
    ├── components/
    │   └── Layout.tsx        # header + <Outlet/>
    ├── pages/
    │   └── HomePage.tsx      # backend /health status card
    └── api/
        ├── client.ts         # axios instance + auth interceptor
        └── health.ts         # getHealth()
```

---

## 4. Key Conventions
- API calls sirf `src/api/` layer se (component me raw axios nahi).
- Server state = TanStack Query; UI state (baad me) = Zustand/Context.
- Feature-based folders Phase 5 se (`features/auth`, `features/tickets`…).
- Token `localStorage` me; axios interceptor har request me Bearer lagata hai.

---

## 5. Verify (Phase 4)
`docker-compose up --build` ke baad http://localhost:5173 kholo →
Home page par **"✅ Backend connected — status: ok, db: true"** dikhna chahiye.

---

## 6. Next
**Phase 5 — Authentication** (login, register, refresh, RBAC, profile) — backend + frontend.
