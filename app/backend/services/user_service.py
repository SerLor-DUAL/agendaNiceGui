# app/backend/services/user_service.py

# Import necessary modules
from backend.models.user.model import User
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import uuid
from backend.utils.hashing import hash_password
from backend.models.user.DTOs import UserCreate

class UserService:
    
    # Gets the next user ID in the database
    async def get_next_user_id(session: AsyncSession) -> int:
        result = await session.exec(select(User.id).order_by(User.id.desc()).limit(1))
        last_id = result.first()
        return (last_id or 0) + 1
    
    # Gets all users
    async def get_all_users(session: AsyncSession) -> list[User]:
        result = await session.exec(select(User))   # Execute a select query to get all users
        return result.all()                         # Get all users from the result 


    # Crates a new user
    async def create_user(userToCreate: UserCreate, session: AsyncSession) -> User:
        new_id = await UserService.get_next_user_id(session)
        
        db_user = User(
            id=new_id,                                              # Set the user's ID to the next available ID
            nickname=userToCreate.nickname,                         # Set the user's nickname
            hashed_password=hash_password(userToCreate.password),   # Hash the user's password
            record_creation=datetime.now(),                         # Set the creation timestamp to the current time
            record_modification=datetime.now()                      # Set the modification timestamp to the current time
        )
        
        session.add(db_user)                # Add the new user to the session
        await session.flush()               # Flush the session to ensure the user is added to the database
        await session.refresh(db_user)      # Refresh the user object to get the latest state from the database
        return db_user


user_Service = UserService()  # Create an instance of UserService to use its methods