from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    is_active: bool = True
