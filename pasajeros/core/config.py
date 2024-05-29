import os
from dotenv import load_dotenv

# Se carga el .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    RABBITMQ_URL: str = os.getenv('RABBITMQ_URL')

# Se instancia los Settings
settings = Settings()