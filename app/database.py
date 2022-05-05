"""coding=utf-8."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://bauti:pass@localhost:5432/usersdb"
SQLALCHEMY_DATABASE_URL = "postgres://uxbnywzimexjuw:360f3d5b31d27e8c9ce22ffbf7a42735808e42ef1805d9a2b77b6a32620af7bd@ec2-52-5-110-35.compute-1.amazonaws.com:5432/d28amjt0el1ome"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()