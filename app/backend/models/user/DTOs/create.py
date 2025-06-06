# app/backend/models/user/DTOs/create.py

from sqlmodel import Field
from backend.models.user.DTOs.base import UserBase

# Definition of the UserCreate DTO model, which is used by the API endpoint to create a new user.
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)    # Original password that will be encrypted before storing