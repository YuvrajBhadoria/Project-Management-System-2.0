from src.data import userData
from src.models.Users import Users

def register(user: Users):
    return userData.register(user)
    
def login(user: Users):
    return userData.login(user)
    
    
def serviceHealth():
    return userData.checkDbHealth()
      