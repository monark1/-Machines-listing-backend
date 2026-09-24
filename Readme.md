# Task — Backend

Python FastAPI service replacing the Angular app's JSON Server mock (`db.json`), backed by MySQL.

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env           
```

Run the schema from the **DB** repo against MySQL instance first — this
service does not create tables itself, it only connects to an existing
database.

## Run

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Project layout

app/
├── main.py # FastAPI app + router wiring
├── core/
│ ├── config.py # env-based settings
│ ├── security.py # password hashing, JWT issue/verify
│ └── query_utils.py # shared pagination, sorting, and search helpers
├── db/
│ ├── base.py # SQLAlchemy declarative base
│ └── session.py # engine, session factory, get_db dependency
├── models/ # SQLAlchemy ORM models (one file per table)
├── schemas/ # Pydantic request/response shapes
│ └── pagination.py # generic PaginatedResponse[T] used by all list endpoints
├── crud/ # DB access functions, one file per entity
└── api/
├── deps.py # auth dependencies (get_current_user, require_roles)
└── routes/ # one router per resource