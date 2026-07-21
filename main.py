from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
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