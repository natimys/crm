from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from app.models import UserRole, PatientStatus


class RussianPhone(PhoneNumber):
    default_region_code = "RU"
    supported_regions = ["RU"]
    phone_format = "E164"

# user schemas
class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=30)
    email: EmailStr
    phone: RussianPhone
    first_name: str = Field(max_length=100)
    second_name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    email: str
    first_name: str
    second_name: str
    surname: str | None
    role: UserRole

# patient + dashboard schemas
class PatientStatusSchema(BaseModel):
    color: str
    label: str
    progress: int

class PatientDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    current_status: PatientStatusSchema

class PatientCreate(BaseModel):
    user_id: int | None = None
    login: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    second_name: str | None = None
    surname: str | None = None
    phone: str | None = None
    password: str | None = None


# checklist schemas
class ChecklistItemUpdate(BaseModel):
    task_id: int
    status: PatientStatus
    value: str | None = None

class PatientChecklistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    task_id: int
    task_title: str
    status: PatientStatus
    value: str | None
    file_path: str | None

class ChecklistCreate(BaseModel):
    operation_type: str
    title: str
    is_required: bool = True

class ChecklistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class IOLRequest(BaseModel):
    k1: float
    k2: float
    axl: float
    a_constant: float = 118.4


# security
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None


class LoginRequest(BaseModel):
    login: str
    password: str
