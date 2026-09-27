RacePulse/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── driver.py
│   │   │   ├── team.py
│   │   │   ├── track.py
│   │   │   ├── race.py
│   │   │   ├── session.py
│   │   │   ├── lap.py
│   │   │   └── telemetry.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── driver.py
│   │   │   ├── race.py
│   │   │   ├── telemetry.py
│   │   │   └── analysis.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── drivers.py
│   │   │   │   ├── races.py
│   │   │   │   ├── telemetry.py
│   │   │   │   └── analysis.py
│   │   │   │
│   │   │   └── dependencies.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── driver_service.py
│   │   │   ├── race_service.py
│   │   │   ├── telemetry_service.py
│   │   │   └── analysis_service.py
│   │   │
│   │   └── database/
│   │       ├── __init__.py
│   │       ├── connection.py
│   │       └── migrations/
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── loaders/
│   │   │   ├── csv_loader.py
│   │   │   └── telemetry_loader.py
│   │   │
│   │   ├── processing/
│   │   │   ├── cleaner.py
│   │   │   ├── transformer.py
│   │   │   └── resampler.py
│   │   │
│   │   ├── analysis/
│   │   │   ├── lap_analysis.py
│   │   │   ├── pace_analysis.py
│   │   │   ├── sector_analysis.py
│   │   │   ├── consistency_analysis.py
│   │   │   └── tyre_analysis.py
│   │   │
│   │   └── visualization/
│   │       ├── speed_trace.py
│   │       ├── lap_chart.py
│   │       └── sector_chart.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_driver.py
│   │   │   ├── test_lap.py
│   │   │   └── test_analysis.py
│   │   │
│   │   └── integration/
│   │       └── test_api.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   │
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   │
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   │
│   │   ├── races/
│   │   │   ├── page.tsx
│   │   │   └── [raceId]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── drivers/
│   │   │   ├── page.tsx
│   │   │   └── [driverId]/
│   │   │       └── page.tsx
│   │   │
│   │   └── telemetry/
│   │       └── page.tsx
│   │
│   ├── components/
│   │   ├── charts/
│   │   │   ├── LapChart.tsx
│   │   │   ├── SpeedTrace.tsx
│   │   │   └── SectorChart.tsx
│   │   │
│   │   ├── dashboard/
│   │   │   ├── StatCard.tsx
│   │   │   └── RaceCard.tsx
│   │   │
│   │   └── ui/
│   │
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── types.ts
│   │
│   ├── public/
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── development.md
│
├── scripts/
│   ├── import_data.py
│   └── seed_database.py
│
└── .github/
    └── workflows/
        ├── tests.yml
        └── deploy.yml