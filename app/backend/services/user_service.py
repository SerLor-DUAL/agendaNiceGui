# app/backend/services/user_service.py

# Import necessary modules
from backend.models.user.model import User                              # Importing the DB User model
from sqlmodel import select                                             # Importing SQLModel for database operations
from sqlmodel.ext.asyncio.session import AsyncSession                   # Importing AsyncSession for asynchronous database operations
from datetime import datetime                                           # Importing for timestamps management
from backend.utils.hashing import hash_handler as hh                    # Importing for password hashing management
from backend.utils.jwt import jwt_handler as jwt                        # Importing for JWT token management
from backend.models.user.DTOs import UserCreate, UserUpdate             # Importing DTOs for user input/output validation and transformation

# NOTE: This class contains functions related to user management which will be used primarly in the API endpoints, but it may contain a few other functions as well 
class UserService:
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Gets the next available user ID by querying the highest current ID
    async def get_next_user_id(session: AsyncSession) -> int:
        
        # Query the database for the highest user ID
        result = await session.exec(select(User.id).order_by(User.id.desc()).limit(1))
        last_id = result.first()
        
        # Return the next ID (last ID + 1), or 1 if no users exist yet
        return (last_id or 0) + 1
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Retrieves all users from the database
    async def get_all_users(session: AsyncSession) -> list[User] | None:
        
        # Query the database for all users and returns a list of them
        result = await session.exec(select(User))
        return result.all()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Creates a new user in the database
    async def create_user(userToCreate: UserCreate, session: AsyncSession) -> User:
        
        # Gets the next ID for the new user
        new_id = await UserService.get_next_user_id(session)
        
        # Creates a new User model instance with provided data and hashed password
        db_user = User(
                            id=new_id,                                                  # Assign new user ID
                            nickname=userToCreate.nickname,                             # Set user nickname
                            hashed_password=hh.hash_password(userToCreate.password),    # Hash the password securely
                            record_creation=datetime.now(),                             # Set creation timestamp to now
                            record_modification=datetime.now()                          # Set modification timestamp to now
                        )
        
        # Adds the new user to the session and flush to assign DB state
        session.add(db_user)
        await session.flush()
        
        # Refresh to get updated DB info
        await session.refresh(db_user)
        
        await session.commit()
        
        # Return the created user      
        return db_user
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Retrieves an user by their ID
    async def read_user_by_id(user_id: int, session: AsyncSession) -> User | None:
        
        # Query the database for a user by their ID and returns it
        result = await session.exec(select(User).where(User.id == user_id))
        return result.first()
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Retrieves an user by their nickname
    async def read_user_by_nickname(nickname: str, session: AsyncSession) -> User | None:
        
        # Query the database for an user by their nickname and returns it
        result = await session.exec(select(User).where(User.nickname == nickname))
        return result.first()
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Updates an existing user's data
    async def update_user(user_id: int, user_to_update: UserUpdate, session: AsyncSession) -> tuple[User | None, bool]:
        
        # Find the user by ID
        user = await UserService.read_user_by_id(user_id, session)
        
        # Initialize updated flag
        updated = False
        
        # If user does not exist, return None and False
        if not user:
            return None, False
        
        # Updates nickname if it's provided and different from the existing one
        if user_to_update.nickname is not None and user.nickname != user_to_update.nickname:
            user.nickname = user_to_update.nickname
            updated = True
        
        # Updates password if it's provided and different from the existing one
        if user_to_update.password:
            if not hh.verify_password(user_to_update.password, user.hashed_password):
                
                # Hash the new password
                user.hashed_password = hh.hash_password(user_to_update.password)
                updated = True
        
        # If no fields were updated, return user with False
        if not updated:
            return user, False
        
        # If update happened, updates modification timestamp and save the changes
        user.record_modification = datetime.now()
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user, updated
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Deletes an existing user by ID
    async def delete_user(user_id: int, session: AsyncSession) -> bool:
        
        # Find the user by ID
        user_to_delete = await UserService.read_user_by_id(user_id, session)
        
        # If user does not exist, return False
        if not user_to_delete:
            return False
        
        # Deletes the user from the database and flush to assign DB state
        await session.delete(user_to_delete)   
        await session.flush()
        return True
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Authenticate a user by nickname and password, returns user if it has valid credentials
    async def authenticate_user(nickname: str, password: str, session: AsyncSession) -> User | None:
        
        # Gets user by nickname
        user_to_authenticate = await UserService.read_user_by_nickname(nickname, session)
        
        # If user does not exist, return None
        if not user_to_authenticate:
            return None
        
        # Verify that the provided password matches the stored password hash
        if not hh.verify_password(password, user_to_authenticate.hashed_password):
            return None
        
        # Return the user if credentials are valid
        return user_to_authenticate
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Login user: verify user credentials and return JWT token if successful
    async def login_user(nickname: str, password: str, session: AsyncSession) -> str | None:
        
        # Authenticate user
        user_to_login = await UserService.authenticate_user(nickname, password, session)
        
        # If user is not authenticated or does not exist, return None
        if not user_to_login:
            return None
        
        # Prepare data to encode in the token
        token_data = {
            "sub": str(user_to_login.id),
            "nickname": user_to_login.nickname
        }
        
        # Creates access and refresh tokens with the token data which contains the user ID and nickname as claims to be used for authentication by middleware
        access_token = jwt.create_access_token(token_data)
        refresh_token = jwt.create_refresh_token(token_data)

        # Return both access and refresh tokens in JWT token
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Creates a single instance of UserService to use throughout the app
user_Service = UserService()
