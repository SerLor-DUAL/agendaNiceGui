from backend.models.event.DTOs.base import EventBase
from datetime import datetime


class EventRead(EventBase):
    id: int
    record_creation: datetime
    record_modification: datetime
    user_id: int
