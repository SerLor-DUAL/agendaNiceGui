# app/backend/services/user_service.py

# Import necessary modules
from backend.models.user.model import User
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from backend.utils.hashing import hash_password, verify_password
from backend.models.user.DTOs import UserCreate, UserUpdate

class UserService:
    
    # Gets the next user ID in the database
    async def get_next_user_id(session: AsyncSession) -> int:
        result = await session.exec(select(User.id).order_by(User.id.desc()).limit(1))
        last_id = result.first()
        return (last_id or 0) + 1
    
    # Gets all users
    async def get_all_users(session: AsyncSession) -> list[User] | None:
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
    
    # Reads an user by ID
    async def read_user_by_id(user_id: int, session: AsyncSession) -> User | None:
        result = await session.exec(select(User).where(User.id == user_id))     # Execute a select query to find the user by ID
        return result.first()
    
    # Updates an existing user
    async def update_user(user_id: int, user_to_update: UserUpdate, session: AsyncSession) -> tuple[User | None, bool]:
        user = await UserService.read_user_by_id(user_id, session) 
        updated = False
        if not user:
            return None                                                         # If the user does not exist, return None
        
        # Update the user's nickname if it's provided and different from the current one
        if user_to_update.nickname is not None and user.nickname != user_to_update.nickname:
            user.nickname = user_to_update.nickname
            updated = True
        
        # Update the user's password if it's provided and different from the current one
        if user_to_update.password:
                if not verify_password(user_to_update.password, user.hashed_password):
                    user.hashed_password = hash_password(user_to_update.password)
                    updated = True
        
        # If no updates were made, return the user as is
        if not updated:
            return user
        
        # If updates were made, set the modification timestamp and save the user
        else:
            user.record_modification = datetime.now()
            session.add(user)
            await session.flush()
            await session.refresh(user)

        return user, updated
    
    # Deletes an existing user
    async def delete_user(user_id: int, session: AsyncSession) -> bool:
        user = await UserService.read_user_by_id(user_id, session)
        if not user:
            return False 
        
        await session.delete(user)      # Delete the user from the session
        await session.flush()           # Flush the session to apply the changes
        return True
    
    
    
user_Service = UserService()  # Create an instance of UserService to use its methods