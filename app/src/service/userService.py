from src.data import userData
from src.models.Users import Users,UserLogin

def register(user: Users):
    return userData.register(user)
    
def login(user: UserLogin):
    return userData.login(user)
    
    
def serviceHealth():
    return userData.checkDbHealth()
      