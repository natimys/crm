from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_patients_by_doctor, create_or_link_patient
from app.models import User, UserRole
from app.dependencies import get_current_user, role_required
from app.engine import get_db
from app.schemas import PatientDashboardResponse, PatientCreate


dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_router.get("/patients", response_model=list[PatientDashboardResponse])
async def get_dashboard_data(
    offset: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    patients = await get_patients_by_doctor(
        doctor_id=current_user.id, 
        role=current_user.role, 
        db=db, 
        limit=limit, 
        offset=offset
    )
    
    return [
        PatientDashboardResponse(
            id=p.id,
            full_name=f"{p.user.surname or ''} {p.user.first_name or ''} {p.user.second_name or ''}".strip(),
            status=p.status,
            color=p.calculated_status[0],
            completion_percent=p.calculated_status[1]
        )
        for p in patients
    ]

@dashboard_router.post("/patients", response_model=PatientDashboardResponse)
async def create_patient_endpoint(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.OPHTALM))
):
    patient = await create_or_link_patient(db, patient_data, current_user.id)
    
    await db.refresh(patient, ["user", "documents", "records"])
    
    color, percent = patient.calculated_status
    
    return {
        "id": patient.id,
        "full_name": f"{patient.user.surname or ''} {patient.user.first_name or ''}".strip(),
        "status": patient.status,
        "color": color,
        "completion_percent": percent
    }
