from pydantic import validator, BaseModel
from datetime import date


class ShareValidator(BaseModel):
    name: str
    date: date
    open: float
    low: float
    high: float
    close: float
    average: float

    class Config:
        orm_mode = True


class CompanyValidator(BaseModel):
    name: str
    description: str = ''
    updated_at: date
    country: str
    currency: str
    initial_date: date

    @validator('country', check_fields=False)
    def capitalize(cls, v):
        if v:
            return v.capitalize()
        return v

    class Config:
        orm_mode = True
