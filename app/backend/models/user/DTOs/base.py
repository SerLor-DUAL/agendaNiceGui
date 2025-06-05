# app/backend/models/user/DTOs/base.py

# Import necessary modules
from sqlmodel import SQLModel, Field

# Definition of the base User DTO model, which contains common fields for user-related operations.
class UserBase(SQLModel):
    nickname: str = Field(..., max_length=100)

    class Config:
        orm_mode = True