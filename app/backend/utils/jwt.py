# app/backend/utils/jwt.py

# Import necessary modules
from datetime import datetime, timedelta                # Importing datetime and timedelta for working with dates
from fastapi import HTTPException                       # Importing HTTPException for error handling
from jose import jwt, JWTError, ExpiredSignatureError   # Importing JWTError for handling JWT decoding errors
from typing import Optional, Dict, Any                  # Importing Optional, Dict, and Any for type hints
import os                                               # Importing os for accessing environment variables

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This constants are extracted from environment variables and are used for JWT creation and decoding

# Secret key for encoding the JWT from environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY")                                
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")

# Algorithm used for encoding the JWT
ALGORITHM = "HS256" 
                
# Token expiration time in minutes                             
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Refresh token expiration time in days
REFRESH_TOKEN_EXPIRE_DAYS = 7                                    

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This class handles JWT creation and decoding
class JWTHandler:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #
    
    # Function to create a JWT with the given data and expiration time
    def create_jwt(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        
        # Creates a copy of the data to encode, set the expiration time, and encode the data into a JWT
        to_encode = data.copy()
        
        # Sets the expiration time for the token, defaulting to ACCESS_TOKEN_EXPIRE_MINUTES if not provided
        expire = datetime.now() + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        
        # Updates the data with the expiration time
        to_encode.update({"exp": expire})
        
        # Encodes the data into a JWT using the secret key and algorithm                                
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        # Returns the encoded JWT                   
        return encoded_jwt

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Function to decode a JWT and return the payload
    def decode_jwt(self, token: str) -> Dict[str, Any]:
        try:
            
            # Decodes the JWT using the secret key and algorithm, then returns the payload
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        
        # Raises an error if the token is expired
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        
        # Returns an empty dictionary if the token is invalid
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #      

# Function to create an access token directly
def create_access_token(self, data: Dict[str, Any]) -> str:
    return self.create_jwt(data)

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #      

# Function to create a refresh token directly
def create_refresh_token(self, data: Dict[str, Any]) -> str:
    return self.create_jwt(data, timedelta(days=self.refresh_token_expire_days))

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #      

# Create an instance of JWTHandler to use throughout the app
jwt_handler = JWTHandler() 