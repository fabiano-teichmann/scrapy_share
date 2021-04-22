from datetime import date

from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.endpoints.validation import CompanyValidation, ShareValidator
from app.models.models import CompanyModel, ShareModel

v1 = APIRouter()


@v1.get('/list_company/{country}')
def get_list_company(country: str = 'brazil'):
    companies = CompanyModel.get_list_companies(country)
    list_companies = []
    for company in companies:
        list_companies.append(CompanyValidation.from_orm(company).dict())
    total_records = companies.count()
    response = {'info': {'total_records': total_records}, 'data': list_companies}
    return JSONResponse(status_code=200, content=response)


@v1.get('/shares')
def get_shares(name: str, date_start: date, date_stop: date):
    try:
        query = ShareModel.get_shares(name, date_start, date_stop)
        shares = []
        for q in query:
            shares.append(ShareValidator.from_orm(q).dict())
        return JSONResponse(status_code=200, content=shares)
    except ValueError as e:
        return JSONResponse(status_code=422, content={'message': f'Something unexpected happened:  {e}'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message':  f'Error get share {e.args}'})
