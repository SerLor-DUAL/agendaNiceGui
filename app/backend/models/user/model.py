# app/backend/models/user/model.py

# Import necessary modules
from sqlmodel import SQLModel, Field, Column, Integer, String, TIMESTAMP         # Importing SQLModel for database operations
from datetime import datetime                                                    # Importing for timestamps management
from typing import Optional                                                      # Importing Optional for type hints
from backend.config import users_table_settings as ut                            # Importing users table settings

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This class model represents an user in the database
class User(SQLModel, table=True):
    
    # Table name
    __tablename__ = ut.USERS_TABLE                
    
    # Primary key column - unique identifier for each user
    id: Optional[int] = Field(default=None, sa_column=Column(ut.USERS_ID_COL, Integer, primary_key=True))
    
    # Nickname column - stores the user's nickname
    nickname: Optional[str] = Field(sa_column=Column(ut.USERS_NICKNAME_COL, String(100), nullable=False))
    
    # Hashed password column - securely stored user password
    hashed_password: Optional[str] = Field(sa_column=Column(ut.USERS_HASHEDPASSWORD_COL, String(500), nullable=False))
    
    # Record creation timestamp - when the user was created
    record_creation: Optional[datetime] = Field(default_factory=datetime.now, sa_column=Column(ut.USERS_RECORDCREATION_COL, TIMESTAMP, nullable=False))
    
    # Record modification timestamp - when the user was last updated
    record_modification: Optional[datetime] = Field(default_factory=datetime.now, sa_column=Column(ut.USERS_RECORDMODIFICATION_COL, TIMESTAMP, nullable=False))
    