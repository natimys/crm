from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_user
from app.engine import get_db
from app.models import User, UserRole
from app.security import decode_token

security = HTTPBearer()


async def get_current_user(
        request: Request,
        db: AsyncSession = Depends(get_db),
    ) -> User:

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authorized"
        )

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )
    
    user = await get_user(int(user_id), db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user