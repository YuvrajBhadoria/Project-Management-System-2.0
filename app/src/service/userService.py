from src.data import userData
from src.models.Users import Users,UserLogin

def register(user):
    result = userData.register(user)

    if result == {"error": "email"}:
        return {"error": "Email already exists"}

    if result == {"error": "username"}:
        return {"error": "Username already exists"}

    return result
    
def login(user: UserLogin):
    return userData.login(user)
    
    
def serviceHealth():
    return userData.checkDbHealth()
    
def getUserById(user_id):
    return userData.getUserById(user_id)

def getUserByUsername(username):
    return userData.getUserByUsername(username)

