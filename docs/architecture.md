# docs/architecture.md

# Architecture

## Status
**Planned / target architecture.** Nothing below is implemented yet — this describes where the project is headed, not what exists today. See `docs/development.md` for what's actually runnable right now.

## System overview

                     ┌─────────────────────┐
                     │       Next.js       │
                     │      Frontend       │
                     └──────────┬──────────┘
                                │ HTTP
                     ┌──────────▼──────────┐
                     │       FastAPI       │
                     │       Backend       │
                     └──────────┬──────────┘
           ┌────────────────────┼────────────────────┐
   ┌───────▼────────┐   ┌──────▼───────┐   ┌──────▼──────┐
   │   PostgreSQL   │   │    Redis     │   │  Analytics  │
   │    Database    │   │    Cache     │   │   Engine    │
   └────────────────┘   └──────────────┘   └──────┬──────┘
                                                   │
                                         ┌─────────▼─────────┐
                                         │ Python Analytics  │
                                         │ NumPy/Pandas/SciPy│
                                         └─────────┬─────────┘
                                                   │
                                         ┌─────────▼─────────┐
                                         │ AI / RAG Layer    │
                                         │    (Planned)      │
                                         └───────────────────┘

## Layers

### `backend/app/` — API layer
- `models/` — domain objects (Driver, Team, Track, Race, Session, Lap, Telemetry). Introduced incrementally; `Driver` first.
- `schemas/` — Pydantic request/response shapes, kept separate from the domain models.
- `api/routes/` — FastAPI route handlers, grouped by resource.
- `services/` — business logic, called by routes, orchestrating models + analytics.
- `database/` — SQLAlchemy engine/session setup, Alembic migrations.

### `backend/analytics/` — Analysis engine
Pure Python/Pandas/NumPy pipeline, independent of the web layer:
`loaders` → `processing` → `analysis` → `visualization`.
This stays the single source of numerical truth — including for the future AI/RAG layer, which explains results rather than computing them.

### `frontend/` — Next.js app
Pages under `app/`, shared UI in `components/`, API client + types in `lib/`.

## Why this split
- Domain models stay separate from Pydantic schemas so the DB/domain shape can evolve without breaking the API contract, and vice versa.
- The analytics engine has no FastAPI/DB dependency, so it can be tested and used standalone (scripts, notebooks) as well as through the API.
- See root `README.md` → "Development Principles" for the reasoning behind avoiding premature abstraction.

For the full planned repository layout, see `Structure.md` in the project root.

## Decisions log
_(Add entries here as real architectural decisions get made — e.g. why Postgres over another DB, sync vs async SQLAlchemy. Empty for now — nothing decided yet beyond what's in the README.)_