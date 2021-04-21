import peewee
import uvicorn
from fastapi import FastAPI
from logger import logger

from app.api import endpoints
from app.models.company import CompanyModel, ShareModel


app = FastAPI(title="API invest")


@app.on_event("startup")
async def start_application():
    try:
        CompanyModel.create_table()
    except peewee.OperationalError:
        logger.info('Table already exists')
    try:
        ShareModel.create_table()
    except peewee.OperationalError:
        logger.info('Table already exists')


app.include_router(
    endpoints.v1,
    tags=["Api invest"],
    prefix='/v1',
    responses={404: {"description": "Not found"}}
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
