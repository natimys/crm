import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Boolean, func, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.engine import Base


class UserRole(str, enum.Enum):
    OPHTALM = "ophtalm"
    SURGEON = "surgeon"
    PATIENT = "patient"
    ADMIN = "admin"


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

class DocumentType(str, enum.Enum):
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
    checklist_items: Mapped[List["PatientChecklist"]] = relationship(lazy="selectin")
    @property
    def calculated_status(self):
        if not self.checklist_items:
            return "red", 0
            
        total_tasks = len(self.checklist_items)
        confirmed_tasks = sum(1 for item in self.checklist_items if item.status == PatientStatus.CONFIRMED)
        loaded_tasks = sum(1 for item in self.checklist_items if item.status == PatientStatus.LOADED)
        
        progress = int((confirmed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        if confirmed_tasks == total_tasks:
            return "green", 100
        
        if (confirmed_tasks + loaded_tasks) == total_tasks:
            return "yellow", progress if progress > 50 else 50
            
        return "red", progress


class PatientDocument(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    
    passport_serial: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    passport_number: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    snils: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    insurance: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

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


class Checklist(Base):
    __tablename__ = "checklists"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation_type: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))
    is_required: Mapped[bool] = mapped_column(Boolean)

class PatientStatus(str, enum.Enum):
    WAITING = "waiting"
    LOADED = "loaded"
    CONFIRMED = "confirmed"

class PatientChecklist(Base):
    __tablename__ = "patient_checklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey("checklists.id"))
    task: Mapped["Checklist"] = relationship(lazy="selectin") 

    status: Mapped[PatientStatus] = mapped_column(
        Enum(PatientStatus, native_enum=False), 
        default=PatientStatus.WAITING,
        nullable=False
    )
    
    file_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    value: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )