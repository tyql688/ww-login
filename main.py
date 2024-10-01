import random
import string
import time
from collections import OrderedDict
from typing import Union

import httpx
from fastapi import FastAPI, APIRouter
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from starlette.responses import HTMLResponse


class TimedCache:
    def __init__(self, timeout=5, maxsize=10):
        self.cache = OrderedDict()
        self.timeout = timeout
        self.maxsize = maxsize

    def set(self, key, value):
        if len(self.cache) >= self.maxsize:
            self._clean_up()
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self._clean_up()
        self.cache[key] = (value, time.time() + self.timeout)

    def get(self, key, default=None):
        if key in self.cache:
            value, expiry = self.cache.pop(key)
            if time.time() < expiry:
                self.cache[key] = (value, expiry)
                return value
        return default if default else None

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def _clean_up(self):
        current_time = time.time()
        keys_to_delete = []
        for key, (value, expiry_time) in self.cache.items():
            if expiry_time <= current_time:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.cache[key]


cache = TimedCache(600, 1000)
app = FastAPI()
waves_router = APIRouter(prefix="/waves", tags=["waves"])
templates = Environment(
    loader=FileSystemLoader("templates")
)


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


@waves_router.post("/token", response_model=TokenModel, status_code=200)
async def generate_token(auth: AuthModel):
    _token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    cache.set(_token, LoginModel(**auth.dict()))
    return {"token": _token}


@waves_router.get("/i/{token}", response_class=HTMLResponse)
async def verify_html(token: str):
    m = cache.get(token)
    template_name = "index.html" if m else "404.html"
    template = templates.get_template(template_name)
    return HTMLResponse(template.render(auth=token, userId=m.user_id) if m else template.render())


@waves_router.post("/login")
async def waves_login(data: LoginModel):
    temp = cache.get(data.auth)
    if temp is None:
        return {"success": False, "msg": "登录超时"}
    ck = await kuro_login(data.mobile, data.code)
    if not ck:
        return {"success": False, "msg": "验证码无效"}
    data.ck = ck
    cache.set(data.auth, data)
    return {"success": True}


@waves_router.post("/get", response_model=LoginModel, status_code=200)
async def waves_login(_token: TokenModel):
    temp = cache.get(_token.token, LoginModel())

    if temp and temp.ck:
        cache.delete(_token.token)

    return temp


app.include_router(waves_router)


async def kuro_login(mobile: str, code: str):
    login_url = "https://api.kurobbs.com/user/sdkLoginForH5"
    headers = {
        "source": "h5",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "devCode": ""
    }
    data = {"mobile": mobile, "code": code}
    async with httpx.AsyncClient() as client:
        res = await client.post(login_url,
                                data=data,
                                headers=headers)
        result = res.json()
        if not isinstance(result, dict) or result.get('code') != 200 or result.get('data') is None:
            return ''
        return result.get('data', {}).get("token", '')
