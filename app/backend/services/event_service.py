# app/backend/services/event_service.py

# Import necessary modules
from backend.models.event.model import Event                            # Importing the DB Event model
from sqlmodel import select                                             # Importing SQLModel for database operations
from sqlmodel.ext.asyncio.session import AsyncSession                   # Importing AsyncSession for asynchronous database operations
from datetime import datetime                                           # Importing for timestamps management
from backend.models.event.DTOs import EventCreate, EventUpdate          # Importing DTOs for event input/output validation and transformation
from backend.models.user.model import User                              # Importing the DB User model        
from sqlalchemy.sql.operators import ilike_op                           # Import ILIKE operator for case-insensitive filtering

# NOTE: This class contains functions related to event management which will be used primarly in the API endpoints, but it may contain a few other functions as well 
class EventService:

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # AUXILIARY METHODS #
    
    async def get_next_event_id(session: AsyncSession) -> int:
        """Gets the next available event ID from the database by querying the highest current ID."""

        # Query the database for the highest event ID
        result = await session.exec(select(Event.id).order_by(Event.id.desc()).limit(1))
        last_id = result.first()
        
        # Return the next ID (last ID + 1), or 1 if no users exist yet  
        return (last_id or 0) + 1
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # CREATE METHODS #
    
    # ------------------------------ #
    # NOTE: METHODS FOR CURRENT USER #
    # ------------------------------ #
    
    async def create_user_event(event_to_create: EventCreate, current_user: User, session: AsyncSession) -> Event:
        """Creates a new event for the current user in the database."""
        
        # Get the next Event ID
        new_id = await EventService.get_next_event_id(session)
        
        # Validates datetime fields
        new_start_date = event_to_create.start_date.replace(tzinfo=None)
        new_end_date = event_to_create.end_date.replace(tzinfo=None)

        # Creates a new Event model instance
        db_event = Event(
            id=new_id,
            title=event_to_create.title,
            description=event_to_create.description,
            start_date=new_start_date,
            end_date=new_end_date,
            user_id=current_user.id,
            record_creation=datetime.now(),
            record_modification=datetime.now()
        )

        # Add the created event to the session
        session.add(db_event)
        return db_event
    
    # --------------------- #
    # NOTE: GENERAL METHODS #
    # --------------------- #
    
    async def create_event(event_to_create: EventCreate, user_id: int, session: AsyncSession) -> Event:
        """Creates a new event in the database."""
        
        # Get the next Event ID
        new_id = await EventService.get_next_event_id(session)
        
        # Validates datetime fields
        new_start_date = event_to_create.start_date.replace(tzinfo=None)
        new_end_date = event_to_create.end_date.replace(tzinfo=None)

        # Creates a new Event model instance
        db_event = Event(
            id=new_id,
            title=event_to_create.title,
            description=event_to_create.description,
            start_date=new_start_date,
            end_date=new_end_date,
            user_id=user_id,
            record_creation=datetime.now(),
            record_modification=datetime.now()
        )

        # Add the created event to the session
        session.add(db_event)
        return db_event
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # READ METHODS #
    
    # ------------------------------ #
    # NOTE: METHODS FOR CURRENT USER #
    # ------------------------------ #
    
    async def read_user_event_by_id(event_id: int, current_user: User, session: AsyncSession) -> Event | None:
        """Retrieves an event by its ID from the database."""

        # Query the database for an event by its ID
        result = await session.exec(select(Event).where(
                                                            Event.id == event_id,
                                                            Event.user_id == current_user.id
                                                        ))
        
        return result.first()
    
    async def read_all_user_events(current_user: User, session: AsyncSession, maxAmount: int) -> list[Event]:
        """Retrieves all events for a the actual user from the database."""
        
        # Query the database for all events from a specific user with its ID
        if maxAmount is not None and maxAmount > 0:
            result = await session.exec(select(Event).where(Event.user_id == current_user.id).limit(maxAmount))
        else:
            result = await session.exec(select(Event).where(Event.user_id == current_user.id))
            
        return result.all()
    
    
    async def read_all_user_events_by_title(title: str, current_user: User, session: AsyncSession) -> list[Event] | None:
        """Retrieves all user events with a specific title from the database."""
    
        # Query the database for an event by its title for the current user
        result = await session.exec(select(Event).where(
                                                            Event.title.ilike(f"%{title}%"),
                                                            Event.user_id == current_user.id
                                                        ))
            
        return result.all()
    
    # --------------------- #
    # NOTE: GENERAL METHODS #
    # --------------------- #
    
    async def read_event_by_id(event_id: int, session: AsyncSession) -> Event | None:
        """Retrieves an event by its ID from the database."""

        # Query the database for an event by its ID
        result = await session.exec(select(Event).where(Event.id == event_id))
        
        return result.first()
    
    
    async def read_all_events_by_user_id(user_id: int, session: AsyncSession) -> list[Event] | None:
        """Retrieves all events for a specific user by user ID from the database."""
        
        # Query the database for all events from a specific user with its ID
        result = await session.exec(select(Event).where(Event.user_id == user_id))
            
        return result.all()
    
    
    async def read_all_events_by_title(title: str, session: AsyncSession) -> list[Event] | None:
        """Retrieves all events with a specific title from the database."""
    
        # Query the database for an event by its title
        result = await session.exec(select(Event).where(ilike_op(Event.title, f"%{title}%")))
        
        return result.all()
    
    
    async def read_all_events(session: AsyncSession, maxAmount: int) -> list[Event] | None:
        """Retrieves all events from the database."""

        # Query the database for all events
        if maxAmount is not None and maxAmount > 0:
            result = await session.exec(select(Event).limit(maxAmount))
        else:
            result = await session.exec(select(Event))
            
        return result.all()
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # UPDATE MEHTODS #
    
    # ------------------------------ #
    # NOTE: METHODS FOR CURRENT USER #
    # ------------------------------ #

    async def update_user_event(event_id: int, event_to_update: EventUpdate, current_user: User, session: AsyncSession) -> Event | None:
        """Updates an existing event from the current user in the database."""
            
        # Find the event by ID
        db_event = await EventService.read_user_event_by_id(event_id, current_user, session)
        if not db_event:
            return None
        
        # Validates datetime fields
        event_to_update.start_date = event_to_update.start_date.replace(tzinfo=None)
        event_to_update.end_date = event_to_update.end_date.replace(tzinfo=None)
        
        # Boolean to check if any field was updated
        was_updated = False
        
        # Updates the event with provided data
        if event_to_update.title is not None:
            db_event.title = event_to_update.title
            was_updated = True
        if event_to_update.description is not None:
            db_event.description = event_to_update.description
            was_updated = True
        if event_to_update.start_date is not None:
            db_event.start_date = event_to_update.start_date
            was_updated = True
        if event_to_update.end_date is not None:
            db_event.end_date = event_to_update.end_date
            was_updated = True
        
        # If no fields were updated, return
        if not was_updated:
            return None
        
        # Updates modification timestamp
        db_event.record_modification = datetime.now()
        
        # Add the updated event to the session
        session.add(db_event)
        
        return db_event
    
    # --------------------- #
    # NOTE: GENERAL METHODS #
    # --------------------- #
    
    async def update_event(event_id: int, event_to_update: EventUpdate, session: AsyncSession) -> Event | None:
        """Updates an existing event in the database."""
            
        # Find the event by ID
        db_event = await EventService.read_event_by_id(event_id, session)
        if not db_event:
            return None
        
        # Validates datetime fields
        event_to_update.start_date = event_to_update.start_date.replace(tzinfo=None)
        event_to_update.end_date = event_to_update.end_date.replace(tzinfo=None)
        
        # Boolean to check if any field was updated
        was_updated = False
        
        # Updates the event with provided data
        if event_to_update.title is not None:
            db_event.title = event_to_update.title
            was_updated = True
        if event_to_update.description is not None:
            db_event.description = event_to_update.description
            was_updated = True
        if event_to_update.start_date is not None:
            db_event.start_date = event_to_update.start_date
            was_updated = True
        if event_to_update.end_date is not None:
            db_event.end_date = event_to_update.end_date
            was_updated = True
        
        # If no fields were updated, return
        if not was_updated:
            return None
        
        # Updates modification timestamp
        db_event.record_modification = datetime.now()
        
        # Add the updated event to the session
        session.add(db_event)
        
        return db_event
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # DELETE METHODS #
    
    # ------------------------------ #
    # NOTE: METHODS FOR CURRENT USER #
    # ------------------------------ #
    
    async def delete_user_event(event_id: int, current_user: User, session: AsyncSession) -> bool:
        """Deletes an event from the current user from the database by its ID."""

        # Find the event by ID
        db_event = await EventService.read_user_event_by_id(event_id, current_user, session)
        if not db_event:
            return False

        # Delete the event
        await session.delete(db_event)  
        
        return True
    
    # --------------------- #
    # NOTE: GENERAL METHODS #
    # --------------------- #
    
    async def delete_event(event_id: int, session: AsyncSession) -> bool:
        """Deletes an event from the database by its ID."""

        # Find the event by ID
        db_event = await EventService.read_event_by_id(event_id, session)
        if not db_event:
            return False

        # Delete the event
        await session.delete(db_event)  
        
        return True
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Creates a single instance of EventService to use throughout the app
event_Service = EventService()
