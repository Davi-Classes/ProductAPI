import os
import dotenv as env
from pydantic_settings import BaseSettings


env.load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')


settings = Settings()
