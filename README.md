# Task API with Supabase Authentication

## Description

A secure REST API built with **FastAPI**, **PostgreSQL**, **Supabase Authentication**, **Redis**, and **Docker Compose**.

The API allows users to register, log in, access protected endpoints using JWT authentication, log out, and perform CRUD operations on tasks. Authentication is handled by Supabase, while PostgreSQL stores application data.

---

## Features

### Authentication

- User Sign Up
- User Login
- JWT Access Token Authentication
- Protected Routes
- User Logout
- Swagger UI Bearer Authentication

### Task Management

- Create a task
- Read all tasks
- Search tasks
- Update a task
- Delete a task
- View task statistics

### Utilities

- Health Check
- Redis Connectivity Check
- Interactive Swagger Documentation

---

## Tech Stack

- FastAPI
- PostgreSQL 16
- SQLAlchemy
- Supabase Auth
- Redis 7
- Docker Compose
- Swagger UI

---

## Project Structure

```
task_api/
│
├── database.py
├── repository.py
├── schemas.py
├── models.py
├── main.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Environment Variables

Create a `.env` file using `.env.example`.

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres:your_password@db:5432/tasks_db
```

> **Important:** Never commit your `.env` file. Only `.env.example` should be tracked by Git.

---

## Running the Project

Clone the repository.

```bash
git clone <your_repository_url>
```

Navigate into the project.

```bash
cd task_api
```

Start the application.

```bash
docker compose up --build
```

The stack starts:

- PostgreSQL
- Redis
- FastAPI

Open:

API

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# Authentication Flow

1. Register a user using:

```
POST /auth/signup
```

2. Log in using:

```
POST /auth/login
```

The response returns:

- access_token
- refresh_token

3. Click **Authorize** in Swagger.

4. Paste the JWT access token.

5. Access protected endpoints.

6. Log out using:

```
POST /auth/logout
```

Authentication is verified using Supabase JWT validation before protected endpoints are executed.

---

# API Endpoints

| Method | Endpoint | Authentication | Description |
|---------|----------|----------------|-------------|
| GET | / | No | API information |
| GET | /health | No | Health check |
| GET | /public/info | No | Public endpoint |
| POST | /auth/signup | No | Register a new user |
| POST | /auth/login | No | Login user |
| POST | /auth/logout | Yes | Logout user |
| GET | /protected/profile | Yes | Current user profile |
| GET | /tasks | No | Get all tasks |
| GET | /tasks/{id} | No | Get one task |
| POST | /tasks | No | Create task |
| PUT | /tasks/{id} | No | Update task |
| DELETE | /tasks/{id} | No | Delete task |
| GET | /stats | No | Task statistics |
| GET | /redis-check | No | Redis connectivity |

---

## Authentication

Protected endpoints require a Bearer Token.

Example:

```
Authorization: Bearer <access_token>
```

If:

- the token is missing,
- malformed,
- expired,
- or invalid,

the API returns

```
401 Unauthorized
```

---

## Swagger UI

FastAPI automatically generates interactive API documentation.

Open:

```
http://localhost:8000/docs
```

Click **Authorize**, paste your access token, and test protected endpoints directly from the browser.

Include your Swagger screenshot below.

```markdown
![Swagger UI](Swagger1.png)
```

---

## Persistence Verification

The application uses PostgreSQL as persistent storage.

Verification:

1. Start the Docker stack.
2. Create a task.
3. Verify the task exists.
4. Stop the containers.

```
docker compose down
```

5. Restart.

```
docker compose up
```

6. Verify the task still exists.

---

## Redis Stretch Goal

Redis was added as an additional service.

The endpoint

```
GET /redis-check
```

confirms communication between FastAPI and Redis.

---
