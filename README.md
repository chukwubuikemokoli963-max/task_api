# Task CRUD API

## Description

A CRUD (Create, Read, Update, Delete) REST API built with FastAPI, backed by PostgreSQL and running as a Docker Compose stack (FastAPI app + Postgres + Redis).

## Features

- Create a task
- Read tasks
- Update a task
- Delete a task
- Search a task using a query parameter
- View task statistics (`/stats`)
- Health check endpoint (`/health`)
- Redis connectivity check (`/redis-check`)
- Interactive Swagger documentation

## Architecture Note

The original implementation (Assignment 2) stored tasks in memory — data was lost every time the server restarted.

This assignment replaces the in-memory store with a PostgreSQL-backed repository (`repository.py`). The service and route logic in `main.py` did not change in shape — only the data access layer was swapped, proving the separation between routes/service and storage.

## Tech Stack

- FastAPI
- PostgreSQL 16
- Redis 7 (stretch goal)
- SQLAlchemy
- Docker Compose

## Setup

1. Copy the environment template and fill in your own values:
```bash
   cp .env.example .env
```
   `.env` is gitignored and never committed — only `.env.example` is tracked.

2. Install dependencies (only needed if running outside Docker):
```bash
   pip install -r requirements.txt
```

## Run the Full Stack

```bash
docker compose up --build
```

This starts three services together: `db` (Postgres), `redis`, and `app` (FastAPI). The app waits for Postgres to report healthy before starting.

Once running, open:
- API root: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

To stop the stack (keeps your data — the Postgres volume is preserved):
```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API information |
| GET | /health | Health check |
| GET | /redis-check | Redis connectivity check |
| GET | /tasks | Get all tasks |
| GET | /tasks?search=Build | Search tasks by title |
| GET | /tasks/{task_id} | Get one task |
| POST | /tasks | Create a task |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |
| GET | /stats | Task statistics (total/done/open) |

## Sample curl Command

```bash
curl -i http://127.0.0.1:8000/tasks
```

## Swagger UI
![Swagger UI](Swagger1.png)

http://127.0.0.1:8000/docs

## Persistence Verification

1. Started the stack with `docker compose up --build`.
2. Created a task via `POST /tasks`.
3. Confirmed it existed via `GET /tasks`.
4. Ran `docker compose down` (containers stopped and removed, volume preserved).
5. Ran `docker compose up` to restart the stack.
6. Ran `GET /tasks` again — the previously created task was still present, confirming data survives an app + container restart.

## Stretch Goal: Redis

A `redis` service was added to `docker-compose.yml`, and a `GET /redis-check` endpoint pings it to confirm connectivity from the FastAPI app.

## Stretch Goal: Index Performance

Seeded `tasks` with 50,000 rows via `generate_series`.

**Before index (Seq Scan):**
Execution Time: 11.097 ms — full scan checking all 50,000 rows to find the match.

**After `CREATE INDEX idx_tasks_title ON tasks(title);`:**
Execution Time: 0.372 ms — direct index lookup, no table scan needed.

~30x faster on an indexed equality lookup.