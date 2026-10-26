# Todo API

A Flask API for user registration, JWT login, and task management.

## Features

- Register users and log in to receive a JWT access token.
- Create, list, search, view, update, and delete tasks.
- Search tasks by user, status, name, and priority. Name searches ignore case
  and match partial names.
- Task priorities: `low`, `medium`, `high`, `urgent`.
- Task statuses: `pending`, `in_progress`, `completed`, `cancelled`.
- Health checks at `/api/health` and `/api/v2/health`.
- Interactive API documentation with Swagger UI.

## Run the app

Requires Python 3.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app runs at `http://localhost:5001` and creates its SQLite database on the
first request.

## Run tests

With the virtual environment active, run all tests:

```bash
pytest -q
python -m pytest
python -m pytest --cov=.
```

## API documentation

Open [Swagger UI](http://localhost:5001/swagger/) to explore and test the API.
The OpenAPI document is available at
[http://localhost:5001/swagger.json](http://localhost:5001/swagger.json).

## Authentication

Registration (`POST /api/v1/register`), login (`POST /api/v1/auth/login`), and
health checks are public. Task endpoints require a JWT access token. Register
and log in with JSON containing `preferred_name` and `password`. Use the token
from the login response in the `Authorization` header:

```http
Authorization: Bearer <access-token>
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Check API health |
| `GET` | `/api/v2/health` | Check API health (v2) |
| `POST` | `/api/v1/register` | Register a user |
| `POST` | `/api/v1/auth/login` | Log in and get an access token |
| `POST` | `/api/v1/tasks` | Create a task |
| `GET` | `/api/v1/tasks/search?user_id={user_id}` | Search tasks; optionally add `status`, `name`, or `priority` |
| `GET` | `/api/v1/users/{user_id}/tasks` | List a user's tasks |
| `GET` | `/api/v1/users/{user_id}/tasks/{task_id}` | Get a task |
| `PUT` | `/api/v1/users/{user_id}/tasks/{task_id}` | Update a task |
| `DELETE` | `/api/v1/users/{user_id}/tasks/{task_id}` | Delete a task |

Most responses use a JSON object with `status`, `message`, and `data`. The task
list and search endpoints return an array of tasks.
