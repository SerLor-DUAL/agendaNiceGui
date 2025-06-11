# app/backend/api/routes/users.py

# Import necessary modules
from fastapi import APIRouter, HTTPException, status, Depends               # Importing FastAPI components for routing and error handling
from backend.db.db_handler import get_session                               # Importing the get_session function to manage database sessions
from sqlmodel.ext.asyncio.session import AsyncSession                       # Importing AsyncSession for asynchronous database operations
from backend.services.user_service import UserService as us                 # Importing the user service for user-related operations                     
from backend.models.user.model import User                                  # Importing the DB User model
from backend.models.user.DTOs import UserCreate, UserRead, UserUpdate       # Importing DTOs for user input/output validation and transformation

# Creates a new API router for user-related endpoints
userRouter = APIRouter(tags=["users"])

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# CREATE ENDPOINTS #

@userRouter.post("/users", response_model=UserRead)
async def api_create_user(user_to_create: UserCreate, session: AsyncSession = Depends(get_session)):
    """ API endpoint to create a new user in the database and returns a UserRead DTO """
    
    # Calls the UserService function to create the user
    user = await us.create_user(user_to_create, session)                    
    
    # If user creation failed, raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    # Returns the created user converted to UserRead DTO
    return UserRead.model_validate(user)

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# READ ENDPOINTS #

@userRouter.get("/users/{user_id}", response_model=UserRead)
async def api_read_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    """ API endpoint to read a user by ID from the database and returns a UserRead DTO """
    
    # Calls the UserService function to get the user by its ID
    user: User | None = await us.read_user_by_id(user_id, session)

    # If user not found, raise an error
    if not user or user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Returns the user converted to UserRead DTO
    return UserRead.model_validate(user)


@userRouter.get("/users", response_model=list[UserRead])
async def api_get_all_users(session: AsyncSession = Depends(get_session)):
    """ API endpoint to get all users from the database and returns a list of UserRead DTOs """
    
    # Calls the UserService function to retrieve all users from the database
    users: list[User] | None = await us.get_all_users(session)                 
    
    # If no users found, raise an error
    if not users or users == [] or users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Convert each User model instance to UserRead DTO for serialization
    return [UserRead.model_validate(user) for user in users]

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# UPDATE ENDPOINTS #

@userRouter.put("/users/{user_id}", response_model=UserRead)
async def api_update_user_by_id(user_id: int, user_to_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    """ API endpoint to update an existing user by ID in the database and returns a UserRead DTO """
    
    # Calls the UserService function to update user data, returns updated user and flags if update occurred
    user, updated = await us.update_user(user_id, user_to_update, session)
    
    # If user do not exists, raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # If no changes were made to the user data, raise an error
    if not updated:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No changes were made to the user")
    
    # Returns the updated user converted to UserRead DTO
    return UserRead.model_validate(user)

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# DELETE ENDPOINTS #

@userRouter.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    """ API endpoint to delete an user by ID from the database and returns a success message """
    
    # Calls the UserService function to delete the user
    deleted = await us.delete_user(user_id, session)
    
    # If user was not found, raise an error
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        # Return a success message (optional, since status code 204 normally has no content)
        return {"detail": "User deleted successfully"}
