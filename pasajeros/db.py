from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Se crea en engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Se crea la sesion de la bd
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Se obtiene la sesion
def get_db():
    # Instance of database session
    db = SessionLocal()
    try:
        yield db
    finally:
        # Close db
        db.close()