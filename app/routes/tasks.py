from fastapi import APIRouter, HTTPException, Response, status
from psycopg2 import Error, IntegrityError
from psycopg2.extras import RealDictCursor

from app.database.connection import get_connection
from app.models.task import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """Create a new task."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, description, completed)
                VALUES (%s, %s, %s)
                RETURNING id, title, description, completed, created_at
                """,
                (task.title, task.description, task.completed),
            )
            new_task = cur.fetchone()
        conn.commit()
        return dict(new_task)
    except Error:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Could not create task.")
    finally:
        if conn:
            conn.close()


@router.get("/")
def get_all_tasks():
    """Retrieve all tasks."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM tasks ORDER BY id
                """
            )
            tasks = cur.fetchall()
        return [dict(task) for task in tasks]
    except Error:
        raise HTTPException(status_code=500, detail="Could not retrieve tasks.")
    finally:
        if conn:
            conn.close()


@router.get("/{task_id}")
def get_task(task_id: int):
    """Retrieve one task by its ID."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM tasks WHERE id = %s
                """,
                (task_id,),
            )
            task = cur.fetchone()

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        return dict(task)
    except Error:
        raise HTTPException(status_code=500, detail="Could not retrieve task.")
    finally:
        if conn:
            conn.close()


@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    """Update the supplied fields of an existing task."""
    updates = task.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    allowed_fields = {"title", "description", "completed"}
    assignments = ", ".join(f"{field} = %s" for field in updates)
    values = list(updates.values()) + [task_id]

    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f"""
                UPDATE tasks SET {assignments}
                WHERE id = %s
                RETURNING id, title, description, completed, created_at
                """,
                values,
            )
            updated_task = cur.fetchone()

        if updated_task is None:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Task not found.")

        conn.commit()
        return dict(updated_task)
    except HTTPException:
        raise
    except Error:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Could not update task.")
    finally:
        if conn:
            conn.close()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task by its ID."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            deleted = cur.rowcount

        if deleted == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Task not found.")

        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Error:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail="Could not delete task.")
    finally:
        if conn:
            conn.close()
