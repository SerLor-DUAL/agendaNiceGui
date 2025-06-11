# app/backend/api/dependencies/auth_cookies.py

# Import necessary modules
from fastapi import Cookie, HTTPException, status, Response, Depends        # Importing FastAPI components for routing and error handling
from sqlmodel.ext.asyncio.session import AsyncSession                       # Importing AsyncSession for asynchronous database operations
from jose import JWTError                                                   # Importing JWTError for handling JWT decoding errors
from backend.db.db_handler import get_session                               # Importing the database session dependency
from typing import Optional                                                 # Importing Optional for type hints
from backend.utils.jwt import jwt_handler as jwt                            # Importing the JWT handler for token operations
from backend.models.user.model import User                                  # Importing the DB User model
from backend.services.user_service import UserService as us                 # Importing the UserService for user operations

# NOTE: This class handles cookie authentication
class AuthCookiesHandler:

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Function to get the current user from the access token cookie
    async def get_current_user_from_cookie(self, access_token: Optional[str] = Cookie(None), session : AsyncSession = Depends(get_session)) -> User:
        # If no access token cookie is found, raise an error that no token cookie was found
        if not access_token:
            raise HTTPException(
                                    status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="No access token cookie found",
                                    headers={"WWW-Authenticate": "Bearer"},
                                )

        try:
            
            # Decodifies the access token
            payload = jwt.decode_jwt(access_token)
            
            # Extracts the user ID ("sub" claim) from the token payload
            user_id = int(payload.get("sub"))
            
            # If user ID is not found in the token, raise an error
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            # Fetch the user from the database using the extracted user ID
            user = await us.read_user_by_id(user_id, session)
            await session.commit()
            await session.refresh(user)   
            
            # If user is not found, raise an error
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Return the current user
            return user
        
        # Raise an error if the token is invalid or expired
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")


    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Function to set the access token cookie
    def set_access_token_cookie(self, response: Response, token: str) -> None:

        # Set the access token cookie values
        response.set_cookie(
                                key="access_token",
                                value=token,
                                httponly=True,
                                secure=True,        # In localhost, secure=False
                                samesite="lax",
                                max_age=900         # 15 minutes for security
                            )

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Function to set the refresh token cookie
    def set_refresh_token_cookie(self, response: Response, token: str):
        response.set_cookie(
                                key="refresh_token",
                                value=token,
                                httponly=True,
                                secure=True,        # In localhost, secure=False
                                samesite="lax",
                                max_age=604800      # 7 days
                            )
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Function to clear the access and refresh token cookies
    def clear_auth_cookies (self, response: Response) -> None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Create an instance of the AuthCookiesHandler class
auth_cookies_handler = AuthCookiesHandler()