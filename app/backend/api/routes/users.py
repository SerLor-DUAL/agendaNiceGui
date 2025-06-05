# app/backend/api/routes/users.py

# Import necessary modules
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from backend.db.db_handler import get_session
from backend.models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession

# Create a new API router for user-related endpoints
router = APIRouter()

# Endpoint to get all the users, expects a list formed by a User model in the request body
@router.get("/users", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User))
    users = result.all()
    
    # If no users are found, raise a 404 HTTP exception
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users