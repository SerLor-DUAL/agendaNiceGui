import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Claves para la firma del JWT (en un entorno real, guarda esta clave en una variable de entorno)
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

# Instancia de passlib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("admin123"))

# "Base de datos" simulada para los usuarios (en una app real usarías una base de datos)
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "$2b$12$.HFZ13HK2dyvEJM1IYLOeuU9pvhcrKQZ6mB/FnmqCXNZnz0LntNR2",  # Hash de "admin123"
    },
    "user": {
        "username": "user",
        "password": "$2b$12$5Cn35aHfB0FLUu7Pj8tkseV2bJnxHgU8jJSa6hhvwotg1PONhV4g2",  # Hash de "user123"
    }
}

# Funciones para manejar la autenticación y el manejo de tokens JWT
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Funciones para obtener usuarios
def get_user(username: str):
    return fake_users_db.get(username)


# Función para autenticar un usuario
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user

# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para decodificar un token
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None