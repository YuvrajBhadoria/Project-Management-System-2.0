from fastapi import APIRouter, HTTPException, status 
from src.service import userService
from src.models.Users import Users,UserLogin
from ..core.security import create_access_token
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
@router.post("/register")
def register(user: Users):
    created_User: Users = userService.register(user)
    if(created_User):
        return created_User
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Enter the details properly"
    )

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    user_id = userService.login(user)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is wrong"
        )

    token = create_access_token(str(user_id))

    return{
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/health")
def health():
    return userService.serviceHealth()  