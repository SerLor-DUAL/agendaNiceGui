# app/backend/api/dependencies/auth_guard.py

# Import necessary modules
from fastapi import Depends, HTTPException, status                  # Importing FastAPI components for dependency injection
from fastapi.security import OAuth2PasswordBearer                   # Importing OAuth2PasswordBearer for token-based authentication
from jose import JWTError                                           # Importing JWTError for handling JWT decoding errors
from backend.utils.jwt import jwt_handler as jwt                    # Importing the JWT handler for token operations
from backend.db.db_handler import get_session                       # Importing the database session dependency
from backend.services.user_service import UserService as us         # Importing the UserService for user operations
from backend.models.user.model import User                          # Importing the DB User model

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: OAuth2PasswordBearer is a FastAPI dependency that extracts the authorization token to protect routes requiring authentication.
        # The tokenUrl parameter specifies the URL where clients (e.g., Swagger UI or OAuth2 clients) request the token. 
        
        # This URL is relative to the server root, not the internal app prefix.
        # So, even if your FastAPI app is mounted under the "/api" prefix, you must include "/api" in the tokenUrl path to point to the correct token endpoint.
        # For example, the full URL will be: http://<host>:<port>/api/login
        # FastAPI uses this relative path for docs generation and OAuth2 workflows.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login") 

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Retrieves the current user based on the JWT token provided in the Authorization header
async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)) -> User:
    
    try:
        # Decode the JWT token to extract the payload
        payload = jwt.decode_jwt(token)
        
        # Extracts the user ID ("sub" claim) from the token payload, converting it to an integer to match the user ID tupe in the database 
        user_id = int(payload.get("sub"))
        
        # If user ID is not found in the token, raise an error
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        
        # Fetch the user from the database using the extracted user ID
        user = await us.read_user_by_id(user_id, session)
        
        # If user is not found, raise an error
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Return the current user
        return user
    
    # Raise an error if the token is invalid or expired
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")  # Handle JWT errors
    
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #