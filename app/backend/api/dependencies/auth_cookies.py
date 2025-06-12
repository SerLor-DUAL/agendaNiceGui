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
import os                                                                   # Importing os for accessing environment variables

# Get the SECURE_COOKIES environment variable and convert it to a boolean
SECURE_COOKIES = os.getenv("SECURE_COOKIES", "false").lower() == "true"

# NOTE: This class handles cookie authentication
class AuthCookiesHandler:

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    async def get_current_user_from_cookie( self, response: Response, access_token: Optional[str] = Cookie(None), 
                                            refresh_token: Optional[str] = Cookie(None), session : AsyncSession = Depends(get_session)) -> User:
        """ Get the current user from the access token cookie """
        
        # If no access token cookie is found, raise an error that no token cookie was found
        if access_token:
            try:
                # Decodes the access token using the JWT handler
                payload = jwt.decode_jwt(access_token)
                user_id = int(payload.get("sub"))

                if not user_id:
                    raise HTTPException(status_code=401, detail="Invalid token")

                user = await us.read_user_by_id(user_id, session)
                await session.commit()
                await session.refresh(user)
                return user

            except JWTError:
                pass

        # If no access token cookie is found, check the refresh token cookie
        if refresh_token:
            user_id = await self.refresh_tokens(refresh_token, response)
            
            # Gets the user from the database using the user_id
            user = await us.read_user_by_id(user_id, session)
            await session.commit()
            await session.refresh(user)
            return user
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid access or refresh token", headers={"WWW-Authenticate": "Bearer"},)
    
    async def refresh_tokens(self, refresh_token: str, response: Response) -> int:
        """ Refresh access and refresh tokens, and return user_id """
        
        try:
            payload = jwt.decode_jwt(refresh_token)
            user_id = int(payload.get("sub"))

            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            new_token_data = {
                                "sub": payload["sub"],
                                "nickname": payload["nickname"],
                            }

            new_access_token = jwt.create_access_token(new_token_data)
            new_refresh_token = jwt.create_refresh_token(new_token_data)

            self.set_access_token_cookie(response, new_access_token)
            self.set_refresh_token_cookie(response, new_refresh_token)

            return user_id

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    def set_access_token_cookie(self, response: Response, token: str) -> None:
        """ Sets the access token cookie """

        # Set the access token cookie values
        response.set_cookie(
                                key="access_token",
                                value=token,
                                httponly=True,
                                secure=SECURE_COOKIES,  # In localhost, secure=False
                                samesite="lax",
                                max_age=900             # 15 minutes for security
                            )

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    def set_refresh_token_cookie(self, response: Response, token: str):
        """ Sets the refresh token cookie """
        
        response.set_cookie(
                                key="refresh_token",
                                value=token,
                                httponly=True,
                                secure=SECURE_COOKIES,  # In localhost, secure=False
                                samesite="lax",
                                max_age=604800          # 7 days
                            )
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    def clear_auth_cookies (self, response: Response) -> None:
        """ Clears the access and refresh token cookies """
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #
# Create an instance of the AuthCookiesHandler class
auth_cookies_handler = AuthCookiesHandler()