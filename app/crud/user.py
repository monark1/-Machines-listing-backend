from sqlalchemy.orm import Session

from app.core.query_utils import apply_search, apply_sort, paginate
from app.models.user import User

SORTABLE_FIELDS = {
    "username": "username",
    "fullName": "full_name",
    "email": "email",
    "department": "department",
    "dateJoined": "date_joined",
    "role": "role",
    "status": "status",
}

SEARCHABLE_COLUMNS = ["username", "full_name", "email", "department", "status"]


def get_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_all_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    role: str | None = None,
    status: str | None = None,
    department: str | None = None,
    search: str | None = None,
    sort: str | None = None,
    order: str = "asc",
) -> tuple[list[User], int]:
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)
    if department:
        query = query.filter(User.department == department)

    query = apply_search(query, User, search, SEARCHABLE_COLUMNS)

    sort_column = SORTABLE_FIELDS.get(sort) if sort else None
    allowed = set(SORTABLE_FIELDS.values())
    query = apply_sort(query, User, sort_column, allowed, order)

    return paginate(query, page, page_size)


def is_username_taken(db: Session, username: str) -> bool:
    return get_by_username(db, username) is not None


def create(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_status(db: Session, user_id: int, status: str) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    user.status = status
    db.commit()
    db.refresh(user)
    return user