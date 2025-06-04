# Variable para mantener el estado del usuario logueado
current_user = None

def setUser(user):
    global current_user
    current_user = user

def getUser():
    return current_user

def logOut():
    global current_user
    current_user = None
