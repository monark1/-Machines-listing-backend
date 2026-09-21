import enum
from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    stakeholder = "stakeholder"
    employee = "employee"


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.employee)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    department = Column(String(100), nullable=False)
    date_joined = Column(String(30), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.active)
