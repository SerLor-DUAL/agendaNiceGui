# app/backend/models/user/DTOs/update.py

# Import necessary modules
from sqlmodel import Field
from typing import Optional
from backend.models.user.DTOs.base import UserBase

# Definition of the UserUpdate DTO model, which is used by the API endpoint to update user data.
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6)