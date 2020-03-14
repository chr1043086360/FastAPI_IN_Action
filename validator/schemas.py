#######################################################################################
# Param Data @
# Return @
# TODO @ 为了避免和model混淆用schema
# *
# !
# ?
#######################################################################################

from typing import List
from pydantic import BaseModel


class UserValidator(BaseModel):
    id: int = None
    username: str
    password: str
    email: str = None
    permission: str = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    scopes: List[str] = []

# TodoList Schema


class TodoBase(BaseModel):
    title: str
    info: str = None


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        # :是声明, =是默认值
        orm_mode = True
