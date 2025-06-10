from backend.models.event.DTOs.base import EventBase
from typing import Optional
from datetime import datetime
from pydantic import field_validator


class EventCreate(EventBase):
    # We add start_date and end_date as required fields
    start_date: datetime  
    end_date: datetime    
