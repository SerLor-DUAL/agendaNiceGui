# app/backend/utils/hashing.py
from passlib.context import CryptContext

# This module provides functions for hashing and verifying passwords using bcrypt.
    # It uses the Passlib library to handle password hashing securely.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a plain password using bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a plain password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)