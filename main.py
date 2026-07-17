from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()
tasks = [
    {
        "id": 1,
        "title": "LearnAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push project to GitHub",
        "done": False
    }
]

original_tasks = [
    {
        "id": 1,
        "title": "LearnAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push project to GitHub",
        "done": False
    }
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.get("/")
def home():
    return {"name": "Task API", "version": "1.0", "endpoits": ["/tasks"] }

@app.get("/health")
def health():
    return{
        "status": "ok"
    }
@app.get("/tasks")
def get_tasks(search: str = None):
    if search:
        result = []
        for task in tasks:
            if search.lower() in task["title"].lower():
                result.append(task)
        return result
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(
        status_code=400,
        detail="Title is required"
    )
    new_task = {
        "id": len(tasks) +1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def task_update(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"]= task_update.title
            task["done"]= task_update.done
            return task
        
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] ==task_id:
            tasks.remove(task)
            return{ 
                "message": "Task deleted successfully"
            }
        
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.get("/stats")
def get_stats():
    total = len(tasks)
    done = 0
    for task in tasks:
        if task["done"]:
            done +=1
    open_tasks = total - done
    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }

@app.post("/reset")
def reset_task():
    global tasks
    tasks = [task.copy() for task in original_tasks]
    return {
        "message": "Tasks have been reset.", 
        "tasks": tasks
    }