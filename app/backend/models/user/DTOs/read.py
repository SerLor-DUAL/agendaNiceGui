# app/backend/models/user/DTOs/read.py

# Import necessary modules
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.models.user.DTOs.base import UserBase

# Definition of the UserRead DTO model, which is used by the API endpoint to read user data.
class UserRead(UserBase):
    id: Optional[int]
    record_creation: Optional[datetime]
    record_modification: Optional[datetime]