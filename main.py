from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from typing import Optional
import models
import schemas
import repository

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/")
def home():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(search: str = None, db: Session = Depends(get_db)):
    return repository.get_tasks(db, search)


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = repository.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", status_code=201, response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    return repository.create_task(db, task.title)


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def task_update(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = repository.update_task(db, task_id, task_update.title, task_update.done)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = repository.delete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return repository.get_stats(db)

import redis as redis_lib
redis_client = redis_lib.Redis(host="redis", port=6379, decode_responses=True)
@app.get("/redis-check")
def redis_check():
    try:
        pong = redis_client.ping()
        return {"redis": "connected", "ping": pong}
    except Exception as e:
        return {"redis": "unreachable", "error": str(e)}

@app.post("/auth/signup", status_code=201)
def signup(email: Optional[str] = Body(None), password: Optional[str] = Body(None)):
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        result = supabase.auth.sign_up({"email": email, "password": password})
        return {"user": result.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(email: Optional[str] = Body(None), password: Optional[str] = Body(None)):
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")