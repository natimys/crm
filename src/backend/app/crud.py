from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.engine import get_db
from app.models import User, Patient
from app.schemas import UserCreate, UserRole
from app.security import get_password_hash


async def get_user(user_id, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_phone(phone: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.phone_number == phone))
    return result.scalar_one_or_none()


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_login(login: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()


async def create_user(user: UserCreate, db: AsyncSession) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        login=user.login,
        email=user.email,
        first_name=user.first_name,
        second_name=user.second_name,
        surname=user.surname,
        phone_number=str(user.phone),
        hashed_password=hashed_password
    )

    db.add(db_user)
    
    await db.commit()
    
    await db.refresh(db_user)

    return db_user

async def get_patients_by_doctor(
        doctor_id: int,
        role: UserRole,
        db: AsyncSession,
        limit: int = 10,
        offset: int = 0
    ):
    query = (select(Patient).options(
        selectinload(Patient.user),
        selectinload(Patient.documents),
        selectinload(Patient.records)
        ).limit(limit).offset(offset)
    )
    if role == UserRole.OPHTALM:
        query = query.where(Patient.doctor_id == doctor_id)
    
    result = await db.execute(query)
    return result.scalars().all()