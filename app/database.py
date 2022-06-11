"""coding=utf-8."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import Settings
import os
import pymongo
import pymongo_inmemory
from dotenv import load_dotenv

load_dotenv()

settings = Settings()

if settings.ENV == "Tests":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(db_user=settings.DB_USER, db_pwd=settings.DB_PWD, db_host=settings.DB_HOST, db_port=settings.DB_PORT, db_name=settings.DB_NAME)

# "postgresql://uxbnywzimexjuw:360f3d5b31d27e8c9ce22ffbf7a42735808e42ef1805d9a2b77b6a32620af7bd@ec2-52-5-110-35.compute-1.amazonaws.com:5432/d28amjt0el1ome"
# if settings.ENV == "development":
#     SQLALCHEMY_DATABASE_URL = "postgresql://bauti:pass@localhost:5432/usersdb"
# elif settings.ENV == "production":
#     SQLALCHEMY_DATABASE_URL = "postgresql://uxbnywzimexjuw:360f3d5b31d27e8c9ce22ffbf7a42735808e42ef1805d9a2b77b6a32620af7bd@ec2-52-5-110-35.compute-1.amazonaws.com:5432/d28amjt0el1ome"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Mongo
if os.getenv("CURRENT_ENVIRONMENT") == "production":
    _client = pymongo.MongoClient(
        f"mongodb+srv://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWD')}@backend-songs.yhk0y.mongodb.net"
        f"/backend-songs?retryWrites=true&w=majority")
    conn = _client.prod
else:
    _client = pymongo_inmemory.MongoClient()
    conn = _client.testdb
