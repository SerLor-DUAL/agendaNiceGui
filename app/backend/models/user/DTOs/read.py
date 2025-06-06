# app/backend/models/user/DTOs/read.py

# Import necessary modules
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.models.user.DTOs.base import UserBase

# Definition of the UserRead DTO model, which is used by the API endpoint to read user data.
class UserRead(UserBase):
    id: Optional[int]                           # Unique identifier for the user
    record_creation: Optional[datetime]         # Timestamp of when the user was created
    record_modification: Optional[datetime]     # Timestamp of when the user was last modified