# app/backend/models/user/DTOs/base.py

# Import necessary modules
from sqlmodel import SQLModel, Field            # Importing SQLModel for database operations

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This DTO (Data Transfer Object) defines the base user model used in the client-side.
        # It includes only the common fields we want to expose, not the full database model.
class UserBase(SQLModel):
    nickname: str = Field(..., max_length=100)  # User's nickname

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # NOTE: The Config class is used to configure the model behavior.
    class Config:
        from_attributes = True  # Enables compatibility with ORM models, allowing the model to be used with SQLModel and Pydantic.
        
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #