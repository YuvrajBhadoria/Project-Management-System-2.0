from fastapi import APIRouter, HTTPException, status 
from src.service import userService
from src.models.Users import Users
router = APIRouter()

@router.post("/register")
def register(user: Users):
    created_User: Users = userService.register(user)
    if(created_User):
        return created_User
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Enter the details properly"
    )

@router.post("/login")
def login(user: Users):
    loggedIn_user: Users = userService.login(user)
    if(loggedIn_user):
        return loggedIn_user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username or password is wrong"
    )

@router.get("/health")
def health():
    return userService.serviceHealth()  