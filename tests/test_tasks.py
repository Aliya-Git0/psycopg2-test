import os
import psycopg2
import pytest
from fastapi.testclient import TestClient
from psycopg2.extras import RealDictCursor

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/task_management_test",
)


@pytest.fixture()
def client(monkeypatch):
    from app.database import connection as db_connection

    def test_get_connection():
        return psycopg2.connect(TEST_DATABASE_URL)

    monkeypatch.setattr(db_connection, "get_connection", test_get_connection)

    conn = psycopg2.connect(TEST_DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS tasks")
        cur.execute("""
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.close()

    from app.main import app
    with TestClient(app) as test_client:
        yield test_client

    conn = psycopg2.connect(TEST_DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS tasks")
    conn.close()


def test_create_read_update_delete_task(client):
    created = client.post("/api/tasks/", json={
        "title": "Test task",
        "description": "Created by pytest",
        "completed": False,
    })
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/api/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Test task"

    updated = client.put(f"/api/tasks/{task_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/api/tasks/{task_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/api/tasks/{task_id}")
    assert missing.status_code == 404


def test_list_tasks(client):
    client.post("/api/tasks/", json={"title": "First task"})
    client.post("/api/tasks/", json={"title": "Second task"})
    response = client.get("/api/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2
