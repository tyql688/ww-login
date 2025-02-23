from typing import Union

from pydantic import BaseModel


class LoginModel(BaseModel):
    auth: str = ""
    mobile: str = ""
    code: str = ""
    ck: Union[str, None] = ""
    user_id: Union[str, None] = ""
    bot_id: Union[str, None] = ""


class AuthModel(BaseModel):
    bot_id: str
    user_id: str


class TokenModel(BaseModel):
    token: str
