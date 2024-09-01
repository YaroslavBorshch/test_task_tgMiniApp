from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    birthday: Optional[str] = None
    tg_info: str


class UserLoadRequest(BaseModel):
    shared_link: Optional[str] = None
    tg_info: str


class ChangeLinkRequest(BaseModel):
    shared_link: str
    tg_id: str


class BasedResponse(BaseModel):
    user_exist: bool
    user_info: dict
    status: int
    message: str
