from sqlalchemy.orm import Session
from app.models.user import User

def get_by_username(db: Session, username: str) -> User | None:
    return  db.query(User).filter(User.username == username).first()

def get_all(db: Session) -> list[User]:
    return db.query(User).all()

def create(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user) 
    return user

def is_username_taken(db: Session, username: str) -> bool:
    return get_by_username(db, username) is not None

def update_Status(db: Session, user_id: int, status: str) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None: return None

    user.status = status
    db.commit()
    db.refresh(user)
    return user
