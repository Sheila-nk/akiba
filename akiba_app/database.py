from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://sheilakahwai:admin@localhost/akiba_app"

# create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# create a class for a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()