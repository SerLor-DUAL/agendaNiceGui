# app/backend/models/user/DTOs/read.py

# Import necessary modules
from typing import Optional                                  # Importing Optional for type hints
from datetime import datetime                                # Importing datetime for working with dates
from backend.models.user.DTOs.base import UserBase           # Importing UserBase

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This DTO (Data Transfer Object) defines the user read model used in the client-side, which includes the user ID, creation and modification timestamps.
class UserRead(UserBase):
    id: Optional[int]                           # Unique identifier for the user
    record_creation: Optional[datetime]         # Timestamp of when the user was created
    record_modification: Optional[datetime]     # Timestamp of when the user was last modified