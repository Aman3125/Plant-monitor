from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
# The readings are saved in a SQLite file called readings.db next to this file
DATABASE_PATH = (BASE_DIR / "readings.db").resolve().as_posix()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# The connection to the database (check_same_thread lets FastAPI use it from many requests)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Makes a new database session for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Every table in models.py is built from this class
class Base(DeclarativeBase):
    pass


# Gives a route a database session and closes it again when the request is done
def get_db():
    with SessionLocal() as db:
        yield db
