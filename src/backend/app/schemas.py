from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from app.models import UserRole


class RussianPhone(PhoneNumber):
    default_region_code = "RU"
    supported_regions = ["RU"]
    phone_format = "E164"


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


class PatientDashboardResponse(BaseModel):
    id: int
    full_name: str
    status: str
    color: str
    completion_percent: int

    model_config = ConfigDict(from_attributes=True)


class PatientCreate(BaseModel):
    user_id: int | None = None
    login: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    second_name: str | None = None
    surname: str | None = None
    phone: str | None = None
    password: str | None = None



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None


class LoginRequest(BaseModel):
    login: str
    password: str
