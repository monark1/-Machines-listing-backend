from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserRegister, UserOut, UserStatusUpdate
from app.crud import user as user_crud
from app.core.security import hash_password
from app.api.deps import require_roles 
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


def to_user_out(user: User) -> UserOut:
    return UserOut(
         id=user.id,
        username=user.username,
        role=user.role.value,
        fullName=user.full_name,
        email=user.email,
        department=user.department,
        dateJoined=user.date_joined,
        status=user.status.value,
    )


@router.get("/check-username/{username}")
def check_username(username: str, db: Session = Depends(get_db)):
    return {"taken": user_crud.is_username_taken(db, username.lower())}


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_roles("admin"))])
def list_users(db: Session = Depends(get_db)):
    return [to_user_out(u) for u in user_crud.get_all(db)]


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if user_crud.is_username_taken(db, payload.username.lower()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")

    new_user = User(
        username= payload.username.lower(),
        hashed_password=hash_password(payload.password),
        role="employee",
        full_name=payload.fullName,
        email=payload.email,
        department=payload.department,
        date_joined=datetime.utcnow().isoformat(),
        status="active",
    )

    created= user_crud.create(db, new_user)
    return to_user_out(created)

@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(require_roles("admin"))])
def update_status(user_id: int, payload: UserStatusUpdate, db: Session= Depends(get_db)):
    updated = user_crud.update_Status(db, user_id, payload.status)
    if updated is None:
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, detail="User not found")
    return to_user_out(updated)