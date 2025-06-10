# app/backend/api/routes/auth.py

# Import necessary modules
from fastapi import APIRouter, HTTPException, status, Depends, Request, Response                   # Importing FastAPI components for routing and error handling
from sqlmodel.ext.asyncio.session import AsyncSession                                              # Importing AsyncSession for asynchronous database operations
from backend.models.user.model import User                                                         # Importing the DB User model
from backend.models.user.DTOs import UserLogin, UserCreate, UserRead                               # Importing DTOs for validating input/output of user data
from fastapi.security import OAuth2PasswordRequestForm                                             # Importing OAuth2PasswordRequestForm for token authentication
from backend.utils.jwt import jwt_handler as jwt                                                   # Importing the JWT handler for token operations
from backend.api.dependencies.auth_cookies import auth_cookies_handler as ach                      # Importing the dependency to manage the authentication cookies
from backend.services.user_service import UserService as us                                        # Importing the user service for user-related operations
from backend.db.db_handler import get_session                                                      # Importing the get_session function to manage database sessions
from backend.api.dependencies.auth_guard import get_current_user                                   # Importing the dependency to get the current user from the generated token    

# Create a new API router for auth-related endpoints
authRouter = APIRouter(tags=["auth"])

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: For now, OAuth2PasswordRequestForm is used for quick testing and compatibility with OAuth2 standard form data.
# Endpoint to authenticate a user using OAuth2 form data, expects username and password, returns a JWT token if credentials are valid
@authRouter.post("/loginOAuth")
async def api_auth_login_OAuth(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    
    #  Calls the UserService login method with username and password to validate and generate token
    token = await us.login_user(form_data.username, form_data.password, session)

    # If token is None, raise an error
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Returns the access token and the refresh token and token type (bearer)
    return {
                "access_token": token['access_token'],
                "refresh_token": token['refresh_token'],
                "token_type": "bearer"
            }


# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Endpoint to authenticate a user using JSON payload, expects username and password, returns a JWT token if credentials are valid
@authRouter.post("/loginJSON")
async def api_auth_login_JSON(data: UserLogin, response: Response, session: AsyncSession = Depends(get_session)):
    
    # Calls the UserService login method with username and password to validate and generate token
    token = await us.login_user(data.nickname, data.password, session)

    # If token is None, raise an error
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Creates cookies with the access and refresh tokens
    ach.set_access_token_cookie(response, token['access_token'])
    ach.set_refresh_token_cookie(response, token['refresh_token'])
    
    # Returns the access token and the refresh token and token type (bearer)
    return {
                "access_token": token['access_token'],
                "refresh_token": token['refresh_token'],
                "token_type": "bearer"
            }

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Endpoint to create/register a new user in the database, accepts user data validated with UserCreate DTO, returns the UserRead DTO
@authRouter.post("/register")
async def api_auth_register(data: UserCreate, session: AsyncSession = Depends(get_session)):

    # Checks if a user with the same nickname already exists to avoid duplicates
    existing_user = await us.read_user_by_nickname(data.nickname, session)
    
    # If user exists, raise an error
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    # Calls the UserService create_user method to create a new user
    user_created = await us.create_user(data, session)

    # Returns the created user (UserCreate DTO)
    return UserRead.model_validate(user_created) 

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Endpoint to retrieve the currently authenticated user's information, requires the user to be authenticated with the token validated
@authRouter.get("/me")
async def api_auth_get_me(current_user: User = Depends(get_current_user)):
    
    # Return a simple dictionary with user ID and nickname for client-side use
    return {"id": current_user.id, "nickname": current_user.nickname}

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Endpoint to retrieve the currently authenticated user's information, requires the user to be authenticated with the token validated using cookies
@authRouter.get("/me-cookie")
async def api_auth_get_me_cookie(current_user: User = Depends(ach.get_current_user_from_cookie)):
    #return {"id": current_user.id, "nickname": current_user.nickname}
    return current_user

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Endpoint to refresh an access token using a refresh token, expects a refresh token, returns a new access token
@authRouter.post("/refresh")
async def api_auth_refresh_tokens(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    # Decodifies the refresh token
    payload = jwt.decode_jwt(refresh_token)

    # Validates the payload
    if not payload or "sub" not in payload or "nickname" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Uses the decoded token data to create a new access token
    new_token_data = {
                        "sub": payload["sub"],
                        "nickname": payload["nickname"]
                    }

    # Creates a new access and refresh tokens for the user
    new_access_token = jwt.create_access_token(new_token_data)
    new_refresh_token = jwt.create_refresh_token(new_token_data)
    
    # Saves cookies with the new refreshed okens
    ach.set_access_token_cookie(response, new_access_token)
    ach.set_refresh_token_cookie(response, new_refresh_token)

    return {"message": "Tokens refreshed"}

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Endpoint to log out the user, clears the cookies
@authRouter.post("/logout")
async def logout(response: Response):
    ach.clear_auth_cookies(response)
    return {"message": "Logged out"}