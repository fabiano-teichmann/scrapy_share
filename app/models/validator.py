from pydantic import validator, BaseModel
from datetime import date


class ShareValidator(BaseModel):
    name: str
    date: date
    open: float
    low: float
    high: float
    close: float


class CompanyValidator(BaseModel):
    name: str
    description: str = ''
    updated_at: date
    country: str
    currency: str

    @validator('country', check_fields=False)
    def capitalize(cls, v):
        if v:
            return v.capitalize()
        return v
