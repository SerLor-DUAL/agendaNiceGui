from fastapi import APIRouter

router = APIRouter()

# Fake temporal DB
usuarios_db = [
    {"id": 1, "nombre": "Juan", "email": "juan@email.com"},
    {"id": 2, "nombre": "María", "email": "maria@email.com"}
]

@router.get("/users")
def get_users():
    """Obtener todos los usuarios"""
    return usuarios_db

@router.post("/users")
def create_user(name: str, email: str):
    """Crear un nuevo usuario"""
    nuevo_usuario = {
        "id": len(usuarios_db) + 1,
        "name": name,
        "email": email
    }
    usuarios_db.append(nuevo_usuario)
    return nuevo_usuario

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Eliminar un usuario"""
    global usuarios_db
    usuarios_db = [u for u in usuarios_db if u["id"] != user_id]
    return {"mensaje": "Usuario eliminado"}
