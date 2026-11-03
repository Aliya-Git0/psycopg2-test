from fastapi import FastAPI
from app.routes.tasks import router as tasks_router

app = FastAPI(
    title="Task Management API",
    description="CRUD APIs using FastAPI, PostgreSQL and psycopg2.",
    version="1.0.0",
)

app.include_router(tasks_router, prefix="/api")


@app.get("/", tags=["Default"])
def root():
    return {"message": "Welcome to the Task Management API"}
