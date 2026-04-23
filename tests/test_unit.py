import pytest
from pydantic import ValidationError
from app.schemas import TaskCreate, TaskUpdate
from app import service

def test_task_create_valid():
    t = TaskCreate(title="Buy groceries", priority="high")
    assert t.title == "Buy groceries" and t.priority == "high"

def test_task_create_default_priority():
    assert TaskCreate(title="Do laundry").priority == "medium"

def test_task_create_empty_title_raises():
    with pytest.raises(ValidationError): TaskCreate(title="")

def test_task_create_blank_title_raises():
    with pytest.raises(ValidationError): TaskCreate(title="   ")

def test_task_create_title_too_long_raises():
    with pytest.raises(ValidationError): TaskCreate(title="x" * 101)

def test_task_create_invalid_priority_raises():
    with pytest.raises(ValidationError): TaskCreate(title="T", priority="urgent")

def test_task_create_description_too_long_raises():
    with pytest.raises(ValidationError): TaskCreate(title="T", description="x" * 501)

def test_task_create_strips_whitespace():
    assert TaskCreate(title="  Clean room  ").title == "Clean room"

def test_task_update_partial_fields():
    d = TaskUpdate(completed=True).model_dump(exclude_unset=True)
    assert "completed" in d and "title" not in d

def test_task_update_invalid_priority_raises():
    with pytest.raises(ValidationError): TaskUpdate(priority="critical")

def test_task_update_valid_priority():
    assert TaskUpdate(priority="low").priority == "low"

def test_task_create_low_priority():
    assert TaskCreate(title="Read", priority="low").priority == "low"

def test_task_create_with_description():
    assert TaskCreate(title="Call", description="Checkup").description == "Checkup"

def test_task_create_empty_description_allowed():
    assert TaskCreate(title="Walk dog", description="").description == ""

def test_task_create_medium_priority():
    assert TaskCreate(title="Ex", priority="medium").priority == "medium"

def test_create_task_in_db(db):
    t = service.create_task(db, TaskCreate(title="Svc", priority="high"))
    assert t.id is not None and t.completed == False

def test_get_task_returns_correct(db):
    c = service.create_task(db, TaskCreate(title="Find me"))
    assert service.get_task(db, c.id).title == "Find me"

def test_get_task_nonexistent_returns_none(db):
    assert service.get_task(db, 9999) is None

def test_delete_task_success(db):
    t = service.create_task(db, TaskCreate(title="Del"))
    assert service.delete_task(db, t.id) == True

def test_delete_task_nonexistent(db):
    assert service.delete_task(db, 9999) == False

def test_get_task_stats_empty(db):
    s = service.get_task_stats(db)
    assert s["total"] == 0 and s["completed"] == 0 and s["pending"] == 0

def test_mark_all_complete(db):
    service.create_task(db, TaskCreate(title="A"))
    service.create_task(db, TaskCreate(title="B"))
    assert service.mark_all_complete(db) == 2
