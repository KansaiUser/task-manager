from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

class TaskCreate(BaseModel):
    title: str

tasks = [
    Task(id=1, title="Learn Nginx", done=False),
    Task(id=2, title="Build a React app", done=True),
]

@app.get("/api/tasks")
def get_tasks():
    return tasks

@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = Task(
        id=max([t.id for t in tasks], default=0) + 1,
        title=task.title,
        done=False,
    )

    tasks.append(new_task)
    return new_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")