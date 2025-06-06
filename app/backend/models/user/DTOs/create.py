# app/backend/models/user/DTOs/create.py

from sqlmodel import Field                          # Importing Field for defining model fields
from backend.models.user.DTOs.base import UserBase  # Importing UserBase

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This DTO (Data Transfer Object) defines the user creation model used in the client-side, which includes the original password.
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)    # Original password that will be encrypted before storing