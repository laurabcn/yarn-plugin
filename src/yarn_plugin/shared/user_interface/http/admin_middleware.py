from fastapi import Header, HTTPException, status

from yarn_plugin.config import settings


async def require_admin(x_admin_secret: str = Header(...)) -> None:
    if x_admin_secret != settings.admin_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin secret")