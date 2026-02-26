from enum import Enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.engine import Base


class UserRole(str, Enum):
    OPHTALM = "ophtalm"
    SURGEON = "surgeon"
    PATIENT = "patient"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(default=UserRole.PATIENT)
    
    phone_number: Mapped[str] = mapped_column(String(20))
    
    first_name: Mapped[str] = mapped_column(String(100), index=True)
    second_name: Mapped[str] = mapped_column(String(100), index=True)
    surname: Mapped[str] = mapped_column(String(100), index=True)
    
    patient_profile: Mapped[Optional["Patient"]] = relationship(
            back_populates="user", uselist=False, foreign_keys="[Patient.user_id]"
        )
    doctor_profile: Mapped[Optional["Doctor"]] = relationship(
            back_populates="user", uselist=False
        )

class DocumentType(str, Enum):
    PASSPORT = "passport"
    INSURANCE = "insurance"
    SNILS = "snils"


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    status: Mapped[str] = mapped_column(default="new")

    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="patient_profile", foreign_keys=[user_id])
    records: Mapped[list["MedicalRecord"]] = relationship(back_populates="patient", lazy="selectin")
    documents: Mapped["PatientDocument"] = relationship(back_populates="patient")


class PatientDocument(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    
    passport_serial: Mapped[str] = mapped_column(String(4))
    passport_number: Mapped[str] = mapped_column(String(6))
    snils: Mapped[str] = mapped_column(String(11))
    insurance: Mapped[str] = mapped_column(String(16))

    patient: Mapped["Patient"] = relationship(back_populates="documents")

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    file_url: Mapped[str] = mapped_column(String(500))
    record_type: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    patient: Mapped[Patient] = relationship(back_populates="records")


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    cabinet: Mapped[Optional[str]] = mapped_column(String(10))

    user: Mapped["User"] = relationship(back_populates="doctor_profile")