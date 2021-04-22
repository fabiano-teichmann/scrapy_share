from datetime import date, datetime
from typing import List

from pydantic import BaseModel, validator


class CompanyValidation(BaseModel):
    name : str
    description: str = ""
    initial_date: str
    country: str
    currency:  str

    @validator('initial_date', pre=True)
    def validator_date(cls, value):
        try:
            return value.isoformat()
        except:
            raise ValueError('Date not valid')

    class Config:
        orm_mode = True


class ShareValidator(BaseModel):
    name: str
    date: str
    open: float
    low: float
    high: float
    close: float
    average: float

    class Config:
        orm_mode = True

    @validator('date', pre=True)
    def validator_date(cls, value):
        try:
            return value.isoformat()
        except:
            raise ValueError('Date not valid')
