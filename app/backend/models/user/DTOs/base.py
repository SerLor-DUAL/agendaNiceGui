# app/backend/models/user/DTOs/base.py

# Import necessary modules
from sqlmodel import SQLModel, Field

# Definition of the base User DTO model, which contains common fields for user-related operations.
class UserBase(SQLModel):
    nickname: str = Field(..., max_length=100)  # User's nickname

    class Config:
        from_attributes = True  # Enables compatibility with ORM models, allowing the model to be used with SQLModel and Pydantic.