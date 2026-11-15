from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from .security import verify_access_token

bearer_scheme = HTTPBearer()

def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme) 
):
    token = credentials.credentials
    
    user_id = verify_access_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    return user_id



