# app/backend/api/routes/users.py

# Import necessary modules
from fastapi import APIRouter, HTTPException, status, Depends               # Importing FastAPI components for routing and error handling
from backend.db.db_handler import get_session                               # Importing the get_session function to manage database sessions
from sqlmodel.ext.asyncio.session import AsyncSession                       # Importing AsyncSession for asynchronous database operations
from backend.services.user_service import UserService as us                 # Importing the user service for user-related operations                     
from backend.models.user.model import User                                  # DB Model
from backend.models.user.DTOs import UserCreate, UserRead, UserUpdate       # DTOs for user operations 

# Create a new API router for user-related endpoints
router = APIRouter()

# Endpoint to get all users, returns a list of UserRead DTOs
@router.get("/users", response_model=list[UserRead])
async def api_get_users(session: AsyncSession = Depends(get_session)):
    
    # Call the get_all_users function from user_service
    users : list[User] | None = await us.get_all_users(session)                 
    
    if not users or users == [] or users == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)                  # Raise an error if no users are found
    
    return [UserRead.model_validate(user) for user in users]                        # Convert User models to UserRead DTOs using model_validate for compatibility

# Endpoint to create a new user, expects a UserCreate DTO and returns an UserRead model
@router.post("/users", response_model=UserRead)
async def api_create_user(user_to_create: UserCreate, session: AsyncSession = Depends(get_session)):
    
    # Control the creation of a new user with a transaction
    async with session.begin():
        user = await us.create_user(user_to_create, session)                        # Call the create_user function from user_service
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)                # Raise an error if user creation fails
    
    return UserRead.model_validate(user)                                            # Convert User model to UserRead DTO using model_validate for compatibility

# Endpoint to read a user by ID, that returns a UserRead DTO
@router.get("/users/{user_id}", response_model=UserRead)
async def api_read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    
    # Calls the read_user_by_id function from user_service to get the user by ID
    user: User | None = await us.read_user_by_id(user_id, session) 

    if not user or user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)                  # Raise an error if the user is not found
    
    return UserRead.model_validate(user)                                            # Convert User model to UserRead DTO using model_validate for compatibility

# Endpoint to update an existing user, expects a UserUpdate DTO and returns an UserRead model
@router.put("/users/{user_id}", response_model=UserRead)
async def api_update_user(user_id: int, user_to_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    
    # Control the update of an existing user with a transaction
    async with session.begin():
        user, updated = await us.update_user(user_id, user_to_update, session)      # Call the update_user function from user_service, returning the updated user
                                                                                    # and a boolean indicating if the user was updated
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)                  # Raise an error if the user is not found
    
    if not updated:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)                 # Raise an error if the user was not updated
    
    return UserRead.model_validate(user)                                            # Convert User model to UserRead DTO using model_validate for compatibility

# Endpoint to delete a user by ID, returns a 204 No Content response if successful
@router.post("/users/{user_id}")
async def api_delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    
    async with session.begin():
            await us.delete_user(user_id, session)                                        # Call the delete_user function from user_service
                                                                                                    # returning a boolean indicating if the user was deleted
    # if not deleted:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")         # Raise an error if the user is not found
