import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    RABBITMQ_URL: str = os.getenv('RABBITMQ_URL')

settings = Settings()