
import uvicorn
from fastapi import FastAPI
from logger import logger

from app.endpoints.endpoint_v1 import v1
from app.models.connect_db import connect_mongodb

app = FastAPI(title="API invest")


@app.on_event("startup")
async def start_application():
    try:
        connect_mongodb()
    except Exception as err:
        logger.warning(f'Error in connect to MongoDB and run initial loads - Error: {err}')


app.include_router(
    v1,
    tags=["Api invest"],
    prefix='/v1',
    responses={404: {"description": "Not found"}}
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
