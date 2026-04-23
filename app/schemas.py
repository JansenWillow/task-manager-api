from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

VALID_PRIORITIES = ["low", "medium", "high"]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=500)
    priority: Optional[str] = Field(default="medium")

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be blank")
        return v.strip()

    @field_validator("priority")
    @classmethod
    def priority_must_be_valid(cls, v):
        if v not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {VALID_PRIORITIES}")
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator("priority")
    @classmethod
    def priority_must_be_valid(cls, v):
        if v is not None and v not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {VALID_PRIORITIES}")
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    completed: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
