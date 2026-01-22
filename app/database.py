from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, DeclarativeBase 

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://smartsort_user:smartsort_pass@localhost:5432/smartsort")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine=create_engine (DATABASE_URL, echo=True)

SessionLocal=sessionmaker (bind=engine,
autocommit=False,
autoflush=False, )

class Base (DeclarativeBase):
    pass 
