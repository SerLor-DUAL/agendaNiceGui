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
    # AUXILIARY METHODS #
    
    async def get_next_user_id(session: AsyncSession) -> int:
        """ Gets the next available user ID from the database by querying the highest current ID. """
            
        # Query the database for the highest user ID
        result = await session.exec(select(User.id).order_by(User.id.desc()).limit(1))
        last_id = result.first()
        
        # Return the next ID (last ID + 1), or 1 if no users exist yet
        return (last_id or 0) + 1

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # CREATE METHODS #

    async def create_user(userToCreate: UserCreate, session: AsyncSession) -> User:
        """ Creates a new user in the database and returns a User model instance """
            
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
        
        # Add the created user to the session
        session.add(db_user)
        
        return db_user
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # READ METHODS #
    
    # Retrieves an user by their ID
    async def read_user_by_id(user_id: int, session: AsyncSession) -> User | None:
        """ Retrieves an user by its ID from the database """

        # Query the database for a user by their ID and returns it
        result = await session.exec(select(User).where(User.id == user_id))
            
        return result.first()
    
    
    async def read_user_by_nickname(nickname: str, session: AsyncSession) -> User | None:
        """ Retrieves an user by their nickname from the database """

        # Query the database for an user by their nickname and returns it
        result = await session.exec(select(User).where(User.nickname == nickname))
            
        return result.first()
    
    
    async def get_all_users(session: AsyncSession) -> list[User] | None:
        """ Gets all users from the database and returns a list of User model instances """
        
        # Query the database for all users and returns a list of them
        result = await session.exec(select(User))
            
        return result.all()
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # UPDATE METHODS #
    
    async def update_user(user_id: int, user_to_update: UserUpdate, session: AsyncSession) -> tuple[User | None, bool]:
        """ Updates an existing user in the database and returns a User model instance and a boolean indicating if update occurred """

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

        # Add the created user to the session
        session.add(user)
        
        return user, updated
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # DELETE METHODS #
    
    async def delete_user(user_id: int, session: AsyncSession) -> bool:
        """ Deletes an user from the database by its ID """

        # Find the user by ID
        user_to_delete = await UserService.read_user_by_id(user_id, session)
        
        # If user does not exist, return False
        if not user_to_delete:
            return False
        
        await session.delete(user_to_delete)
        
        return True
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    # AUTHENTICATION METHODS #
    
    async def authenticate_user(nickname: str, password: str, session: AsyncSession) -> User | None:
        """ Verifies that the provided password matches the stored password hash from the database """

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
    
    
    async def login_user(nickname: str, password: str, session: AsyncSession) ->  dict[str, str] | None:
        """ Authenticates a user using their nickname and password. If the credentials are valid,
            generates and returns a pair of JWT tokens (access and refresh)."""
        
        # Authenticate user
        user_to_login = await UserService.authenticate_user(nickname, password, session)
        print(user_to_login)
        
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
