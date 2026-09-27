# docs/api.md

# API Reference

## Status
**Not implemented yet** — FastAPI hasn't been introduced (Phase 3). This file lists the *planned* endpoint surface from the roadmap, so it doubles as a lightweight spec while you build.

Once the backend is running, FastAPI auto-generates live interactive docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Those become the source of truth for request/response schemas — plan to trim this file down to a short pointer to them, rather than hand-maintaining a duplicate list, once Phase 3 lands.

## Planned endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/drivers` | List drivers |
| GET | `/api/races` | List races |
| GET | `/api/races/{race_id}` | Race detail |
| GET | `/api/telemetry/{session_id}` | Telemetry for a session |
| POST | `/api/telemetry/upload` | Upload telemetry data |
| GET | `/api/analysis/{session_id}` | Computed analysis for a session |

Endpoint names aren't final — per the README's Phase 3 note: *"Do not finalize endpoint names until requirements are clear."*

## Conventions (once implemented)
- Request/response bodies validated via Pydantic schemas in `backend/app/schemas/`.
- Errors returned as standard FastAPI `HTTPException` JSON bodies.
- Auth (Phase 6) will add a bearer-token requirement to endpoints that need it — none do yet.