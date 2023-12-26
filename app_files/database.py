from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQL_ALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# connect_args only needed for SQLlite, not for other DBs.
# use it to allow multiple threads to connect to DB, not a single thread (defs/asynch defs)
# will give each thread its own session explicitly in this app
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
