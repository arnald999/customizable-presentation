from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.user_store import get_or_create_user_id

security = HTTPBearer(auto_error=True)  # Enables Swagger "Authorize" button

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user_id = get_or_create_user_id(token)  # Use Bearer token like before
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API token")

    request.state.user_id = user_id
    return user_id
