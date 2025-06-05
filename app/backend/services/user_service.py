# app/backend/services/user_service.py

# Import necessary modules
from backend.models.user import User
from backend.db.db_handler import async_session

# Async function to create a new user in the database
async def create_user(user: User) -> User:
    """Create a new user in the database."""
    
    async with async_session() as session:
        async with session.begin():         # Start a new transaction
            session.add(user)               # Add the user to the session      
        await session.commit()              # Commit the transaction
        await session.refresh(user)         # Refresh the user instance to get the updated state
    return user