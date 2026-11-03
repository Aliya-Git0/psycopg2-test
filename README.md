# Task Management API — FastAPI + psycopg2

A beginner-friendly CRUD REST API using FastAPI and PostgreSQL through the psycopg2 driver. No ORM is used: SQL statements and database operations are written explicitly.

## Endpoints

| Method | URL | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/` | Retrieve all tasks |
| GET | `/api/tasks/{task_id}` | Retrieve one task |
| PUT | `/api/tasks/{task_id}` | Update a task |
| DELETE | `/api/tasks/{task_id}` | Delete a task |

Swagger documentation: `http://127.0.0.1:8000/docs`

## 1. Requirements

- Python 3.10+
- PostgreSQL installed and running
- pip

## 2. Create the PostgreSQL database

Open pgAdmin Query Tool or `psql` and execute:

```sql
CREATE DATABASE task_management;
```

Connect to the new `task_management` database, then execute the contents of `database/schema.sql`.

Optional sample data: execute `database/seed.sql`.

## 3. Set up Python environment

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and provide the PostgreSQL password and username.

## 4. Run the API

From the project root:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and try the endpoints.

## 5. Example JSON

Create task (`POST /api/tasks/`):

```json
{
  "title": "Learn FastAPI",
  "description": "Build a CRUD API using psycopg2",
  "completed": false
}
```

Update task (`PUT /api/tasks/1`):

```json
{
  "title": "Learn FastAPI and PostgreSQL",
  "completed": true
}
```

The update endpoint accepts partial fields, so the caller can update only `completed`, for example.

## 6. Run tests

Create a separate test database:

```sql
CREATE DATABASE task_management_test;
```

Set its connection string in PowerShell:

```powershell
$env:TEST_DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/task_management_test"
pytest -v
```

**Warning:** The tests drop and recreate the `tasks` table in the configured test database. Never point `TEST_DATABASE_URL` at a production or important database.

## How psycopg2 is used

1. `psycopg2.connect()` opens a PostgreSQL connection.
2. `connection.cursor()` creates a cursor to execute SQL.
3. `cursor.execute(query, parameters)` runs parameterized SQL.
4. `fetchone()` retrieves one row; `fetchall()` retrieves multiple rows.
5. `connection.commit()` saves a successful write.
6. `connection.rollback()` cancels a failed write.
7. `connection.close()` releases the connection.

The `%s` placeholders are psycopg2 parameter placeholders. Do not concatenate user-provided values into SQL statements.

## Project structure

```text
fastapi-psycopg2-task-api/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   └── task.py
│   └── routes/
│       └── tasks.py
├── database/
│   ├── schema.sql
│   └── seed.sql
├── tests/
│   └── test_tasks.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

This is a focused educational assignment project. It intentionally omits authentication and unrelated features so the CRUD and psycopg2 concepts remain clear.
