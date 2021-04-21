import time
from datetime import date

from fastapi import APIRouter
from logger import logger
from starlette.responses import JSONResponse

from app.api.company import get_list_companies, get_share

v1 = APIRouter()


@v1.get('/list_company/{country}')
def get_list_company(country: str = 'brazil'):
    return get_list_companies(country)


@v1.get('/shares')
def get_shares(name: str, date_start: date, date_stop: date):
    try:
        start = time.time()
        payload = get_share(name, date_start, date_stop)
        stop = time.time()
        logger.info(f"Time {round(stop - start, 5)}")
        return payload
    except ValueError as e:
        return JSONResponse(status_code=422, content={'message': f'Something unexpected happened:  {e}'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message':  f'Error get share {e.args}'})


@v1.post('/buy_share')
def buy_share():
    pass

