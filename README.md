# Yo Watch This!

A full-stack video recommendation app — share YouTube, Vimeo, Spotify, SoundCloud and Dailymotion links with friends, rate what you watch, and reply to recommendations.

## Stack

| | Tech |
|---|---|
| **Frontend** | React 18, Vite, React Router, Axios, PWA |
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL (Supabase) |
| **Auth** | JWT (python-jose), bcrypt |
| **Tests** | pytest (backend), Vitest + Testing Library (frontend) |
| **Deploy** | Vercel (frontend) · Render (backend) · Supabase (database) |

## Structure

```
ywt/
├── frontend/        # React + Vite SPA
└── backend/         # FastAPI REST API
    ├── app/
    │   ├── core/        # config, security, exceptions
    │   ├── db/          # SQLAlchemy models + session
    │   ├── schemas/     # Pydantic schemas
    │   ├── repositories/
    │   ├── services/
    │   └── routers/
    ├── tests/
    └── scripts/
```

## Backend

```bash
make install     # install dependencies
make run         # start dev server
make test        # run test suite
make lint        # flake8
make db-seed     # seed database with test data
```

## Frontend

```bash
npm install          # install dependencies
npm run dev          # start dev server
npm run test:run     # run test suite (single pass)
npm run test         # run test suite (watch mode)
npm run build        # production build
```

## Local setup

1. Clone the repo and create a `.env` in `backend/` :

```env
DATABASE_URL=sqlite:///./dev.db
JWT_SECRET_KEY=your-secret-key
```

2. Create a `.env` in `frontend/` :

```env
VITE_API_URL=http://localhost:8000
```

3. Start both servers :

```bash
# terminal 1
cd backend && make run

# terminal 2
cd frontend && npm run dev
```
