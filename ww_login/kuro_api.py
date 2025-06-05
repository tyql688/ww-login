import uuid
from typing import Optional, Union

import httpx
from httpx import HTTPError


async def kuro_login(mobile: str, code: str) -> Union[Optional[str], Optional[str]]:
    """
    Login to Kuro API with mobile and verification code.

    Args:
        mobile: User's mobile number
        code: Verification code

    Returns:
        str: Authentication token if successful, None otherwise
    """
    login_url = "https://api.kurobbs.com/user/sdkLogin"
    headers = {
        "source": "ios",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "devCode": "",
    }
    did = str(uuid.uuid4()).upper()
    data = {"mobile": mobile, "code": code, "devCode": did}

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(login_url, data=data, headers=headers)
            res.raise_for_status()
            result = res.json()

            if not isinstance(result, dict):
                return None, None

            if result.get("code") != 200 or not result.get("data"):
                return None, None

            return result.get("data", {}).get("token"), did

    except (HTTPError, ValueError):
        return None, None
