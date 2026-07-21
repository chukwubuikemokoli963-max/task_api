from sqlalchemy.orm import Session
from sqlalchemy import func
import models


def get_tasks(db: Session, search: str = None):
    query = db.query(models.Task)
    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))
    return query.all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, title: str):
    new_task = models.Task(title=title, done=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, task_id: int, title: str, done: bool):
    task = get_task(db, task_id)
    if task is None:
        return None
    task.title = title
    task.done = done
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if task is None:
        return None
    db.delete(task)
    db.commit()
    return task


def get_stats(db: Session):
    total = db.query(models.Task).count()
    done = db.query(models.Task).filter(models.Task.done == True).count()
    return {"total": total, "done": done, "open": total - done}