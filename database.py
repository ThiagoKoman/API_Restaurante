from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_database, sessionmaker

DATABASE_URL = "sqlite:///./restaurante.db"
engine = create_engine(DATABASE_URL, echo=True,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
