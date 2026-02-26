from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserResponse, Token, LoginRequest
from app.crud import get_user_by_email, get_user_by_phone, get_user_by_login, create_user
from app.engine import get_db
from app.security import verify_password, create_access_token
from app.models import User, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    if await get_user_by_phone(user.phone, db):
        raise HTTPException(
            status_code=400,
            detail="Phone already registered"
        )
    if await get_user_by_login(user.login, db):
        raise HTTPException(
            status_code=400,
            detail="Login already registered"
        )
    return await create_user(user, db)


@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_login(credentials.login, db)

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect login or password"
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token)


@router.get("/debug/users", response_model=List[UserResponse])
async def get_all_users_debug(db: AsyncSession = Depends(get_db)):
    query = select(User)
    
    result = await db.execute(query)
    
    users = result.scalars().all()
    
    return users

@router.patch("/set-role/{user_id}")
async def set_user_role(
    user_id: int, 
    new_role: UserRole, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = new_role
    await db.commit()
    return {
            "status": "success", 
            "new_role": user.role
            }
