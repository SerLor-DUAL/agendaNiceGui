from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class EventBase(SQLModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    # id is not included as not every event will have it.
    

    class Config:
        from_attributes = True