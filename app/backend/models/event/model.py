# app/backend/models/event/model.py

# Import necessary modules
from sqlmodel import SQLModel, Field, Column, Integer, String, TIMESTAMP, ForeignKey    # Importing SQLModel for database operations
from datetime import datetime                                                           # Importing for timestamps management
from typing import Optional                                                             # Importing Optional for type hints
from backend.config import events_table_settings as et                                  # Importing events table settings
from backend.config import users_table_settings as ut                                   # Importing users table settings for using the fk

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This class model represents an event in the database
class Event(SQLModel, table=True):
    
    # Table name
    __tablename__ = et.EVENTS_TABLE
    
    # Primary key column - unique identifier for each user
    id: Optional[int] = Field(default = None, sa_column = Column(et.EVENTS_ID_COL, Integer, primary_key = True))
    
    # Title column - stores the event title
    title: Optional[str] = Field(default = None, sa_column = Column(et.EVENTS_TITLE_COL, String(100), nullable = False))
    
    # Description column - stores the event description
    description: Optional[str] = Field(sa_column = Column(et.EVENTS_DESCRIPTION_COL, String(500), nullable = True))

    # Start date column - stores the start date of the event
    start_date: Optional[datetime] = Field(default_factory=datetime.now, sa_column = Column(et.EVENTS_STARTTIME_COL, TIMESTAMP, nullable = False))
    
    # End date column - stores the end date of the event
    end_date: Optional[datetime] = Field(default_factory=datetime.now,sa_column = Column(et.EVENTS_ENDTIME_COL, TIMESTAMP, nullable = False))
    
    # User ID column - foreign key referencing the user table
    user_id: Optional[int] = Field(default = None, sa_column = Column(et.EVENTS_USER_ID_COL, Integer, ForeignKey(ut.USERS_ID_COL)))
    
    # Record creation timestamp - when the user was created
    record_creation: Optional[datetime] = Field(default_factory=datetime.now, sa_column = Column(et.EVENTS_RECORDCREATION_COL, TIMESTAMP, nullable = False))
    
    # Record modification timestamp - when the user was last updated
    record_modification: Optional[datetime] = Field(default_factory=datetime.now, sa_column = Column(et.EVENTS_RECORDMODIFICATION_COL, TIMESTAMP, nullable = False))