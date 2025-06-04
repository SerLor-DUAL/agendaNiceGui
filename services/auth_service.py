# Ejemplo de usuarios "en memoria"
users_db = {
    'admin': '1234',  # Username: admin, Password: 1234
    'user': 'password'  # Username: user, Password: password
}

def authenticateUser(username, password):
    # Verifica si el usuario existe y si la contraseña es correcta
    if username in users_db and users_db[username] == password:
        return True
    return False
