from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    MONGODB_URI: str = Field(env='MONGODB_URI')
