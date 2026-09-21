from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.crud import user as user_crud

bearer_scheme= HTTPBearer

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db),
):
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid or Expired Token")

    user = user_crud.get_by_username(db, payload.get("sub"))
    if payload is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(*allowed_roles: str):
    def checker(current_user = Depends(get_current_user)):
        if current_user.roles.value not in allowed_roles:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Insufficient permission")
        return current_user
    return checker
          
