# docs/development.md

# Development Guide

## Status
Reflects the current state as of Phase 1 (initial setup). See root `README.md` → "Development Roadmap" for the full phase plan.

## Prerequisites
- Python 3.x
- Git
- Docker & Docker Compose (for Postgres/Redis — optional until you're actually using them)
- Node.js + npm (only needed from Phase 5 onward, frontend)

## Getting the code
```bash
git clone <repository-url>
cd RacePulse
```

## Environment variables
Copy the example file and fill in real values locally:
```bash
cp .env.example .env
```
Never commit `.env` — it's already covered by the root `.gitignore`.

## Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
`requirements.txt` is organized by phase — only the current phase's block is uncommented. Uncomment a block (and re-run `pip install -r requirements.txt`) only when you actually reach that phase.

## Local infrastructure (Postgres + Redis)
```bash
docker compose up -d
```
Starts Postgres on `localhost:5432` and Redis on `localhost:6379`, matching the defaults in `.env.example`. The `backend`/`frontend` services in `docker-compose.yml` stay commented out until their Dockerfiles have real content (Phase 3 / Phase 5).

## Running tests
```bash
cd backend
pytest
```
`backend/tests/` is scaffolded but empty right now — first tests land alongside the `Driver` model.

## Git conventions
Conventional Commits:

feat: add Driver model
fix: handle missing telemetry values
refactor: separate telemetry processing
test: add lap analysis tests
docs: update setup instructions
chore: dependency bump

Avoid vague messages like `update`, `changes`, `final`.

## Current project status
🚧 Early development — only the repository skeleton, `.env.example`, `docker-compose.yml` (Postgres/Redis), and phase-gated `requirements.txt` exist. No application code has been written yet.