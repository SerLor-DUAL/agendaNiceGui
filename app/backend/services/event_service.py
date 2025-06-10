# Import necessary modules
from backend.models.event.model import Event                            # Importing the DB Event model
from sqlmodel import select                                             # Importing SQLModel for database operations
from sqlmodel.ext.asyncio.session import AsyncSession                   # Importing AsyncSession for asynchronous database operations
from datetime import datetime                                           # Importing for timestamps management
# Importing DTOs for event input/output validation and transformation
from backend.models.event.DTOs.create import EventCreate
from backend.models.event.DTOs.update import EventUpdate  
from backend.models.user.DTOs.read import UserRead                        # Importing the DB User model        
from sqlalchemy.sql.operators import ilike_op                                            # Import ilike for case-insensitive filtering

class EventService:

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # CREATE
    async def get_next_event_id(session: AsyncSession) -> int:
        """Gets the next available event ID by querying the highest current ID."""
        result = await session.exec(select(Event.id).order_by(Event.id.desc()).limit(1))
        last_id = result.first()
        return (last_id or 0) + 1
    
    async def create_event(event_to_create: EventCreate, session: AsyncSession) -> Event:
        """Creates a new event in the database."""


        # Get the next Event ID
        new_id = await EventService.get_next_event_id(session)
        
        # Validate datetime fields
        new_start_date = event_to_create.start_date.replace(tzinfo=None)
        new_end_date = event_to_create.end_date.replace(tzinfo=None)

        # Create a new Event model instance.
        db_event = Event(
            # Assign new ID
            id=new_id,
            # Set event with provided data
            title=event_to_create.title,
            description=event_to_create.description,
            start_date=new_start_date,
            end_date=new_end_date,
            user_id=2,  # Use the current user's ID
            # Set creation and modification timestamps to now
            record_creation=datetime.now(),
            record_modification=datetime.now()
        )
        
        session.add(db_event)
        await session.flush()
        await session.refresh(db_event)
        await session.commit()
    
        return db_event
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # READ
    async def read_all_events(session: AsyncSession, maxAmount: int) -> list[Event] | None:
        """Retrieves all events from the database."""
        if maxAmount is not None and maxAmount > 0:
            result = await session.exec(select(Event).limit(maxAmount))
        else:
            result = await session.exec(select(Event))
        return result.all()
    
    # Basic Filters for reading events.
    async def read_event_by_id(event_id: int, session: AsyncSession) -> Event | None:
        """Retrieves an event by its ID."""
        result = await session.exec(select(Event).where(Event.id == event_id))
        return result.first()
    
    async def read_event_by_user_id(user_id: int, session: AsyncSession) -> list[Event] | None:
        """Retrieves all events for a specific user by user ID."""
        result = await session.exec(select(Event).where(Event.user_id == user_id))
        return result.all()
    
    async def read_event_by_title(title: str, session: AsyncSession) -> list[Event] | None:
        """Retrieves all events with a specific title."""
        result = await session.exec(select(Event).where(ilike_op(Event.title, f"%{title}%")))
        return result.all()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # UPDATE
    async def update_event(event_id: int, event_to_update: EventUpdate, session: AsyncSession) -> Event | None:
        """Updates an existing event in the database."""
        db_event = await EventService.read_event_by_id(event_id, session)
        if not db_event:
            return None
        
        event_to_update.start_date = event_to_update.start_date.replace(tzinfo=None)
        event_to_update.end_date = event_to_update.end_date.replace(tzinfo=None)

        wasUpdated = False
        # Update the event with provided data
        if event_to_update.title is not None:
            db_event.title = event_to_update.title
            wasUpdated = True
        if event_to_update.description is not None:
            db_event.description = event_to_update.description
            wasUpdated = True
        if event_to_update.start_date is not None:
            db_event.start_date = event_to_update.start_date
            wasUpdated = True
        if event_to_update.end_date is not None:
            db_event.end_date = event_to_update.end_date
            wasUpdated = True
        
        if not wasUpdated:
            return None
        
        # Update modification timestamp
        db_event.record_modification = datetime.now()
        session.add(db_event)
        await session.flush()
        await session.refresh(db_event)
        await session.commit()
        return db_event
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    async def delete_event(event_id: int, session: AsyncSession) -> bool:
        """Deletes an event from the database by its ID."""
        db_event = await EventService.read_event_by_id(event_id, session)
        if not db_event:
            return False
        
        await session.delete(db_event)
        await session.commit()
        return True