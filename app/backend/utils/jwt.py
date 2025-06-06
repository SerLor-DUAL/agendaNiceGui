# app/backend/utils/jwt.py

# Import necessary modules
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Dict, Any
import os

# Constants for JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")                                # Secret key for encoding the JWT from environment variable
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")     # Raise an error if the secret key is not set

ALGORITHM = "HS256"                                                     # Algorithm used for encoding the JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30                                        # Token expiration time in minutes

# Class for handling JWT operations
class JWTHandler:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        
# Function to create a JWT with the given data and expiration time
def create_jwt(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()                                                                         # Create a copy of the data to encode                                                       
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))     # Set the expiration time for the token, defaulting to ACCESS_TOKEN_EXPIRE_MINUTES if not provided
    to_encode.update({"exp": expire})                                                               # Update the data with the expiration time                                  
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)                            # Encode the data into a JWT using the secret key and algorithm
    return encoded_jwt

# Function to decode a JWT and return the payload
def decode_jwt(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])                             # Decode the JWT using the secret key and algorithm
        return payload
    except JWTError:
        return {}                                                                                   # Return an empty dictionary if decoding fails

jwt_handler = JWTHandler()  # Instance of the JWTHandler class