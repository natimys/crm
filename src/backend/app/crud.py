from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException

from app.engine import get_db
from app.models import User, Patient, PatientDocument, PatientChecklist, Checklist
from app.schemas import UserCreate, UserRole, PatientCreate, ChecklistCreate
from app.security import get_password_hash


async def get_user(user_id, db: AsyncSession = Depends(get_db)) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_phone(phone: str, db: AsyncSession = Depends(get_db)) -> User | None:
    result = await db.execute(select(User).where(User.phone_number == phone))
    return result.scalar_one_or_none()


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_login(login: str, db: AsyncSession = Depends(get_db)) -> User | None:
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()


async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
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
    query = (
        select(Patient)
        .options(
            selectinload(Patient.user),
            selectinload(Patient.documents),
            selectinload(Patient.records)
        )
        .limit(limit)
        .offset(offset)
    )

    if role == UserRole.OPHTALM:
        query = query.where(Patient.doctor_id == doctor_id)
    
    result = await db.execute(query)
    return result.scalars().all()

async def create_or_link_patient(patient_data: PatientCreate, doctor_id: int, db: AsyncSession = Depends(get_db)):
    if patient_data.user_id:
        target_user_id = patient_data.user_id
        existing_patient = await db.execute(
            select(Patient).where(Patient.user_id == target_user_id)
        )
        if existing_patient.scalars().first():
            raise HTTPException(status_code=400, detail="User already have medical card")
    
    else:
        if not patient_data.login or not patient_data.password:
            raise HTTPException(status_code=400, detail="Login and password required")
            
        new_user = User(
            login=patient_data.login,
            email=patient_data.email,
            hashed_password=get_password_hash(patient_data.password),
            first_name=patient_data.first_name,
            second_name=patient_data.second_name,
            surname=patient_data.surname,
            phone_number=patient_data.phone,
            role=UserRole.PATIENT
        )
        db.add(new_user)
        await db.flush()
        target_user_id = new_user.id

    new_patient = Patient(
        user_id=target_user_id,
        doctor_id=doctor_id,
        status="new"
    )
    db.add(new_patient)
    await db.flush()

    new_docs = PatientDocument(patient_id=new_patient.id)
    db.add(new_docs)

    await db.commit()
    await db.refresh(new_patient)
    return new_patient

async def update_checklist_item(
        patient_id: int,
        update_data: ChecklistCreate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PatientChecklist)
        .where(PatientChecklist.patient_id == patient_id)
        .where(PatientChecklist.task_id == update_data.task_id)
    )
