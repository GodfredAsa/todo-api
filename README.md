# Todo API

A Flask REST API for registering users, authenticating with JWTs, and managing
user tasks.

## Requirements

- Python 3
- Dependencies listed in `requirements.txt`

## Setup and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The server listens on `http://localhost:5001`. The SQLite database is configured
as `data.db` and the application creates its tables on the first request.

## Swagger / OpenAPI documentation

The interactive Swagger UI is served by the application at
[`http://localhost:5001/swagger/`](http://localhost:5001/swagger/). The OpenAPI
3.0 specification is defined in Python in `swagger_docs.py` and is served at
[`http://localhost:5001/swagger.json`](http://localhost:5001/swagger.json).
Use Swagger UI's **Try it out** feature to test endpoints. For protected
operations, first log in, copy the access token from the response's `data`
field, select **Authorize**, and enter the token.

## Authentication

`POST /api/v1/register` and `POST /api/v1/auth/login` are public. The health
endpoint (`GET /api/health`) is also public. Task creation, task listing, task
retrieval, updates, and deletion require a JWT access token.

Register with JSON:

```json
{
  "preferred_name": "Alex",
  "password": "your-password"
}
```

Log in with the same fields. The successful login response places the access
token in `data`. Send it on protected endpoints as:

```http
Authorization: Bearer <access-token>
```

API responses use the following format:

```json
{
  "status": 200,
  "message": "Request successful",
  "data": {}
}
```

The user's task list endpoint returns an array of task objects directly.

## Endpoints

| Method | Path | Authentication | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/health` | No | Check API health |
| `POST` | `/api/v1/register` | No | Register a user |
| `POST` | `/api/v1/auth/login` | No | Log in and receive an access token |
| `POST` | `/api/v1/tasks` | Bearer JWT | Create a task |
| `GET` | `/api/v1/tasks/search?user_id={user_id}` | Bearer JWT | Search a user's tasks by optional status, name, and priority filters |
| `GET` | `/api/v1/users/{user_id}/tasks` | Bearer JWT | List a user's tasks |
| `GET` | `/api/v1/users/{user_id}/tasks/{task_id}` | Bearer JWT | Get a task |
| `PUT` | `/api/v1/users/{user_id}/tasks/{task_id}` | Bearer JWT | Update a task |
| `DELETE` | `/api/v1/users/{user_id}/tasks/{task_id}` | Bearer JWT | Delete a task |

Task priority values are `low`, `medium`, `high`, and `urgent`. Task status
values are `pending`, `in_progress`, `completed`, and `cancelled`. When creating
a task, priority defaults to `medium` and status defaults to `pending`.

The task search endpoint requires `user_id`. Optional `status`, `name`, and
`priority` query parameters can be combined. Name matching is case-insensitive
and supports partial matches.
