from typing import Optional, Set
from pydantic import BaseModel, BaseConfig, Field

class Size(BaseModel):
    nike: int
    adidas: int
    newBalance: int
    vans: int
    converse: int

class User(BaseModel):
    userId: int = Field(title="user_id")
    userName: str = Field(title="사용자 이름")
    age: int = Field(title="사용자 나이")
    gender: str = Field(title="사용자 성별")
    email: str = Field(title="사용자 이메일")
    id: str = Field(title="사용자 아이디")
    shoesSizes: Optional[Size] = None

class UserLogin(BaseModel):
    id: str = Field(title="사용자 아이디")
    password: str = Field(title="사용자 비밀번호")

class UserCreate(BaseModel):
    userName: str = Field(title="사용자 이름")
    age: int = Field(title="사용자 나이")
    gender: str = Field(title="사용자 성별")
    email: str = Field(title="사용자 이메일")
    id: str = Field(title="사용자 아이디")
    password: str = Field(title="사용자 비밀번호")
    shoesSizes: Optional[object] = None
