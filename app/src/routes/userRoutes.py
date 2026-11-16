from fastapi import APIRouter,Response, HTTPException, status, Depends 
from src.service import userService as service
from src.models.Users import Users,UserLogin
from ..core.security import create_access_token
from pydantic import BaseModel
from ..core.dependencies import get_current_user

from src.core.security import (
    create_access_token,
    COOKIE_NAME,
    COOKIE_HTTP_ONLY,
    COOKIE_SECURE,
    COOKIE_SAMESITE,
    COOKIE_MAX_AGE
)

router = APIRouter()

class AuthResponse(BaseModel):
    message: str
    
@router.post("/register")
def register(user: Users):
    created_User: Users = service.register(user)
    if(created_User):
        return created_User
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Enter the details properly"
    )
    

@router.post("/login",response_model= AuthResponse)
def login(user: UserLogin,response:  Response):
    user_id = service.login(user)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is wrong"
        )

    token = create_access_token(str(user_id))

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=COOKIE_MAX_AGE,
        path="/"
    )
    
    return{
        "message": "login successful"
    }
    
@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {"message": "Logged out successfully"}

@router.get("/health",dependencies=[Depends(get_current_user)])
def health():
    return service.serviceHealth()  