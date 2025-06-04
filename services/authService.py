import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

# Claves para la firma del JWT (en un entorno real, guarda esta clave en una variable de entorno)
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

# Instancia de passlib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# "Base de datos" simulada para los usuarios (en una app real usarías una base de datos)
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "$2b$12$5Cn35aHfB0FLUu7Pj8tkseV2bJnxHgU8jJSa6hhvwotg1PONhV4g2",  # Hash de "admin123"
    },
    "user": {
        "username": "user",
        "password": "$2b$12$5Cn35aHfB0FLUu7Pj8tkseV2bJnxHgU8jJSa6hhvwotg1PONhV4g2",  # Hash de "user123"
    }
}

# Función para verificar si la contraseña es correcta
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token JWT para el usuario autenticado
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener el usuario de la base de datos simulada
def get_user(username: str):
    if username in fake_users_db:
        return fake_users_db[username]
    return None

# Función para autenticar el usuario
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and verify_password(password, user["password"]):
        return user
    return None
