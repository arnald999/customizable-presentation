from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.stores.user_store import get_or_create_user_id

security = HTTPBearer()

def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = get_or_create_user_id(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API token")
    request.state.user_id = user_id
    return user_id
