from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, DeclarativeBase 

DATABASE_URL = (
    "postgresql+psycopg2://"
    "smartsort_user:smartsort_pass@localhost:5432/smartsort"
)

engine=create_engine (DATABASE_URL, echo=True)

SessionLocal=sessionmaker (bind=engine,
autocommit=False,
autoflush=False, )

class Base (DeclarativeBase):
    pass 
