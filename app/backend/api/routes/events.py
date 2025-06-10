# Import necessary modules
from fastapi import APIRouter, HTTPException, status, Depends               # Importing FastAPI components for routing and error handling
from backend.db.db_handler import get_session                               # Importing the get_session function to manage database sessions
from sqlmodel.ext.asyncio.session import AsyncSession                       # Importing AsyncSession for asynchronous database operations
from backend.services.event_service import EventService as es               # Importing the event service for event-related operations                     
from backend.models.event.model import Event                                # Importing the DB Event model
# Importing DTOs for user input/output validation and transformation
from backend.models.event.DTOs.create import EventCreate                    
from backend.models.event.DTOs.read import EventRead
from backend.models.event.DTOs.update import EventUpdate

# Create a new API router for user-related endpoints
event_router = APIRouter(tags=["events"])

# CREATE
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# Create a new user, expect a UserCreate DTO and return an EventRead DTO
@event_router.post("/events", response_model=EventRead)
async def api_create_event(event_to_create: EventCreate, session: AsyncSession = Depends(get_session)):

    # Validate datetime fields
    if not event_to_create.start_date or not event_to_create.end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date and end date are required.")

    if event_to_create.start_date >= event_to_create.end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be after end date.")

    # Start Transaction.
    async with session.begin():
        event = await es.create_event(event_to_create, session)
    # If event creation failed, raise an error
    if not event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event creation failed")
    
    return EventRead.model_validate(event)
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# READ
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# Endpoint to get all events, returns a list of EventRead DTOs
@event_router.get("/events", response_model=list[EventRead])
async def api_get_events(session: AsyncSession = Depends(get_session)):

    # Retrieves all events from the database.
    events: list[Event] | None = await es.read_all_events(session)

    # If no events found, raise an error
    if not events or events == [] or events is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
    
    # Convert each Event model instance to EventRead DTO for serialization
    return [EventRead.model_validate(event) for event in events]

# Endpoint to read an event by ID. Returns EventRead DTO
@event_router.get("/events/{event_id}", response_model=EventRead)
async def api_read_event_by_id(event_id: int, session: AsyncSession = Depends(get_session)):

    # Calls the EventService function to get the event by its ID
    event: Event | None = await es.read_event_by_id(event_id, session)

    # If event not found, raise an error
    if not event or event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    return EventRead.model_validate(event)
# Endpoint to read events by user ID. Returns a list of EventRead DTOs
@event_router.get("/events/user/{user_id}", response_model=list[EventRead])
async def api_read_event_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    # Calls the EventSerice to get all events by user ID
    events: list[Event] | None = await es.read_event_by_user_id(user_id, session)
    # If no events found, raise an error
    if not events or events == [] or events is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found for this user")
    
    return [EventRead.model_validate(event) for event in events]
# Endpoint to read events by title. Returns a list of EventRead DTOs
@event_router.get("/events/title/{title}", response_model=list[EventRead])
async def api_read_event_by_title(title: str, session: AsyncSession = Depends(get_session)):
    # Calls the EventService to get all events by title
    events: list[Event] | None = await es.read_event_by_title(title, session)
    
    # If no events found, raise an error
    if not events or events == [] or events is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found with this title")
    
    return [EventRead.model_validate(event) for event in events]

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# UPDATE
@event_router.put("/events/{event_id}", response_model=EventRead)
async def api_update_event(event_id: int, event_to_update: EventUpdate, session: AsyncSession = Depends(get_session)):

    # Begin transaction
    async with session.begin():
        
        # Calls the EventService function to update the event
        event = await es.update_event(event_id, event_to_update, session)

    # If event update failed, raise an error
    if not event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event update failed")
    return EventRead.model_validate(event)
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# DELETE
@event_router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_event(event_id: int, session: AsyncSession = Depends(get_session)):
    # Begin transaction
    async with session.begin():
        
        # Calls the EventService function to delete the event
        was_deleted = await es.delete_event(event_id, session)

    # If event deletion failed, raise an error
    if not was_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found or deletion failed")
    
    return {"detail": "Event deleted successfully"}