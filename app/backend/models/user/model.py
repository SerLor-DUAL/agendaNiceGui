# app/backend/models/user/model.py

# Import necessary modules
from sqlmodel import SQLModel, Field, Column, Integer, String, TIMESTAMP
from datetime import datetime
from typing import Optional

# Configuration with real table and column names from .env
from backend.config import users_table_settings as ut 

# Definition of the User model from the DB
class User(SQLModel, table=True):
    
    # Table name
    __tablename__ = ut.USERS_TABLE                
    
    # Primary key column - unique identifier for each user
    id: Optional[int] = Field(default = None, sa_column = Column(ut.USERS_ID_COL, Integer, primary_key = True))
    
    # Nickname column - stores the user's nickname
    nickname: Optional[str] = Field(sa_column = Column(ut.USERS_NICKNAME_COL, String(100)))
    
    # Hashed password column - securely stored user password
    hashed_password: Optional[str] = Field(sa_column = Column(ut.USERS_HASHEDPASSWORD_COL, String(500)))
    
    # Record creation timestamp - when the user was created
    record_creation: Optional[datetime] = Field(sa_column = Column(ut.USERS_RECORDCREATION_COL, TIMESTAMP))
    
    # Record modification timestamp - when the user was last updated
    record_modification: Optional[datetime] = Field(sa_column = Column(ut.USERS_RECORDMODIFICATION_COL, TIMESTAMP))
    