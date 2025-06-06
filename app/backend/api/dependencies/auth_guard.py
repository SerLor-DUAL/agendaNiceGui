# app/backend/api/dependencies/auth_guard.py

# Import necessary modules
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from backend.utils.jwt import decode_jwt
from backend.db.db_handler import get_session
from backend.services.user_service import UserService as us

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Define the token URL

# Gets the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    try:
        payload = decode_jwt(token)                         # Decode the JWT token
        user_id = payload.get("sub")                        # Get the user ID from the token payload
        
        if user_id is None:
            raise HTTPException(
                                    status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail="Invalid authentication credentials",
                                    headers={"WWW-Authenticate": "Bearer"}
                                )
        
        user = await us.read_user_by_id(user_id, session)   # Fetch the user from the database
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")  # Handle JWT errors