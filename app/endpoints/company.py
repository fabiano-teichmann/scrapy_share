from datetime import date

from mongoengine import Q
from starlette.responses import JSONResponse

from app.models.models import CompanyModel, ShareModel


def get_list_companies(country: str):
    qs = CompanyModel.get_company(name=country)
    company = []
    if qs:
        for q in qs:
            company.append({
                'name': q.name,
                'description': q.description,
            })
        return JSONResponse(status_code=200, content=company)
    return JSONResponse(status_code=204)


def get_share(name: str, date_start: date, date_stop: date):
    qs = ShareModel.objects(name=name)
    data = qs.filter((Q(date__gte=date_start) & Q(date__lte=date_stop)))
    payload = []
    for p in data:
        payload.append({
            'date': p.date.isoformat(),
            'average': p.average
        })
    if payload:
        return JSONResponse(status_code=200, content=payload)
    return JSONResponse(status_code=204)
