# app/backend/api/routes/users.py

# Import necessary modules
from fastapi import APIRouter, HTTPException, Depends                       # Importing FastAPI components for routing and error handling
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
    users = await us.get_all_users(session)                                     # Call the get_all_users function from user_service
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")           # Raise an error if no users are found
    
    return users

# Endpoint to create a new user, expects a UserCreate DTO and returns an User model
@router.post("/users", response_model=User)
async def api_create_user(userToCreate: UserCreate, session: AsyncSession = Depends(get_session)):
    
    # Control the creation of a new user with a transaction
    async with session.begin():
        user = await us.create_user(userToCreate, session)                          # Call the create_user function from user_service
    
    if not user:
        raise HTTPException(status_code=400, detail="User creation failed")         # Raise an error if user creation fails
    
    return user 