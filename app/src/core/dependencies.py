from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..service import userService as service
from .security import verify_access_token

bearer_scheme = HTTPBearer()

def get_current_user(req: Request):
    
    token =req.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
        
    user_id = verify_access_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )
        
    user = service.getUserById(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not user[4]:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    return user



