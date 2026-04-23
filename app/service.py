from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, completed: Optional[bool] = None, priority: Optional[str] = None):
    q = db.query(models.Task)
    if completed is not None:
        q = q.filter(models.Task.completed == completed)
    if priority is not None:
        q = q.filter(models.Task.priority == priority)
    return q.all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description or "", priority=task.priority or "medium")
    db.add(db_task); db.commit(); db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task: return None
    for f, v in task_data.model_dump(exclude_unset=True).items():
        setattr(db_task, f, v)
    db.commit(); db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task: return False
    db.delete(db_task); db.commit()
    return True

def get_task_stats(db: Session):
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.completed == True).count()
    return {"total": total, "completed": completed, "pending": total - completed}

def mark_all_complete(db: Session):
    updated = db.query(models.Task).filter(models.Task.completed == False).update({"completed": True})
    db.commit()
    return updated
