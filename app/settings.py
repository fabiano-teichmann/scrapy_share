from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    MONGODB_URI = Field(env='MONGODB_URI')
