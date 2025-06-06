# app/backend/utils/hashing.py

# Import necessary modules
from passlib.context import CryptContext    # Importing CryptContext for password hashing

# NOTE: This class handles password hashing and verification 
class HashHandler:

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    # Initialize the password hashing context

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Hash a plain password using bcrypt
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Verifies a plain password against a hashed password
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Create an instance of HashHandler to use throughout the app
hash_handler = HashHandler()