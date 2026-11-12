from sqlalchemy import create_engine
from sqlalchemy.orm import declative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./fila.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit = False, autoFlush = False, bind = engine)

Base = declative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()