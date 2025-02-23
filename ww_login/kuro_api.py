from typing import Optional

import httpx
from httpx import HTTPError


async def kuro_login(mobile: str, code: str) -> Optional[str]:
    """
    Login to Kuro API with mobile and verification code.

    Args:
        mobile: User's mobile number
        code: Verification code

    Returns:
        str: Authentication token if successful, None otherwise
    """
    login_url = "https://api.kurobbs.com/user/sdkLoginForH5"
    headers = {
        "source": "h5",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "devCode": "",
    }
    data = {"mobile": mobile, "code": code}

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(login_url, data=data, headers=headers)
            res.raise_for_status()
            result = res.json()

            if not isinstance(result, dict):
                return None

            if result.get("code") != 200 or not result.get("data"):
                return None

            return result.get("data", {}).get("token")

    except (HTTPError, ValueError):
        return None
