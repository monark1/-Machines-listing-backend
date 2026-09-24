from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.security import hash_password
from app.crud import user as user_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import UserRegister, UserOut, UserStatusUpdate

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


@router.get("", response_model=PaginatedResponse[UserOut], dependencies=[Depends(require_roles("admin"))],)
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    role: str | None = None,
    status_: str | None = Query(None, alias="status"),
    department: str | None = None,
    search: str | None = None,
    sort: str | None = None,
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    users, total = user_crud.get_all_paginated(
        db,
        page=page,
        page_size=page_size,
        role=role,
        status=status_,
        department=department,
        search=search,
        sort=sort,
        order=order,
    )
    return PaginatedResponse[UserOut](
        items=[to_user_out(u) for u in users],
        total=total,
        page=page,
        pageSize=page_size,
        totalPages=max(1, -(-total // page_size)),
    )


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if user_crud.is_username_taken(db, payload.username.lower()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    new_user = User(
        username=payload.username.lower(),
        hashed_password=hash_password(payload.password),
        role="employee",
        full_name=payload.fullName,
        email=payload.email,
        department=payload.department,
        date_joined=datetime.utcnow().isoformat(),
        status="active",
    )
    created = user_crud.create(db, new_user)
    return to_user_out(created)


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(require_roles("admin"))],
)
def update_status(
    user_id: int, payload: UserStatusUpdate, db: Session = Depends(get_db)
):
    updated = user_crud.update_status(db, user_id, payload.status)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return to_user_out(updated)