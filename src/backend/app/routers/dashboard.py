from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_patients_by_doctor, create_or_link_patient, update_checklist_item
from app.models import User, UserRole, PatientChecklist, PatientStatus
from app.dependencies import get_current_user, role_required
from app.engine import get_db
from app.schemas import PatientDashboardResponse, PatientCreate, IOLRequest, ChecklistItemUpdate, PatientStatusSchema
from app.iol_calc import calculate_srkt

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
    
    result = []
    for p in patients:
        color, progress = p.calculated_status
        
        labels = {
            "red": "Сбор анализов",
            "yellow": "На проверке",
            "green": "Готов к операции"
        }
        
        status_obj = PatientStatusSchema(
            color=color,
            label=labels.get(color, "new"),
            progress=progress
        )
        
        result.append(PatientDashboardResponse(
            id=p.id,
            full_name=f"{p.user.surname or ''} {p.user.first_name or ''} {p.user.second_name or ''}".strip(),
            current_status=status_obj
        ))
    return result

@dashboard_router.post("/patients", response_model=PatientDashboardResponse)
async def create_patient_endpoint(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.OPHTALM))
):
    patient = await create_or_link_patient(patient_data, current_user.id, db)
    await db.refresh(patient, ["user"])
    
    color, progress = patient.calculated_status
    
    labels = {
        "red": "Analyses collection",
        "yellow": "On verification",
        "green": "Ready"
    }

    status_obj = PatientStatusSchema(
        color=color,
        label=labels.get(color, "Новый"),
        progress=progress
    )
    
    return PatientDashboardResponse(
        id=patient.id,
        full_name=f"{patient.user.surname or ''} {patient.user.first_name or ''}".strip(),
        current_status=status_obj
    )

@dashboard_router.post("/calculate-iol")
async def get_iol_calculation(data: IOLRequest):
    try:
        result = calculate_srkt(data.k1, data.k2, data.axl, data.a_constant)
        return {
            "recommended_power": result,
            "formula": "SRK/T",
            "status": "success"
        }
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Error: Division by zero")


@dashboard_router.post("/checklist/{item_id}/confirm")
async def confirm_analysis(
    item_id: int,
    approve: bool,
    comment: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.SURGEON))
):
    if current_user.role not in [UserRole.OPHTALM, UserRole.SURGEON]:
        raise HTTPException(status_code=403, detail="No permissions")
    
    result = await db.execute(
        select(PatientChecklist).where(PatientChecklist.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    if approve:
        item.status = PatientStatus.CONFIRMED
    else:
        item.status = PatientStatus.WAITING
        item.value = comment
        
    await db.commit()
    return {"status": "updated", "new_item_status": item.status}



