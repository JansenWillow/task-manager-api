from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, service
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task Manager API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Task Manager API is running", "version": "1.0.0"}

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def list_tasks(completed: Optional[bool] = Query(None), priority: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return service.get_tasks(db, completed=completed, priority=priority)

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return service.create_task(db, task)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    t = service.get_task(db, task_id)
    if not t: raise HTTPException(404, "Task not found")
    return t

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    t = service.update_task(db, task_id, task_data)
    if not t: raise HTTPException(404, "Task not found")
    return t

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not service.delete_task(db, task_id):
        raise HTTPException(404, "Task not found")

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return service.get_task_stats(db)
