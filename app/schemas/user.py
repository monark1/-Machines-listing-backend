from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    password: str
    fullName: str
    email: EmailStr
    department: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    fullName: str
    email: str
    department: str
    dateJoined: str
    status: str


class UserStatusUpdate(BaseModel):
    status: str
