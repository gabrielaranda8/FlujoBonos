from os import environ

import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

pymysql.install_as_MySQLdb()
Base = declarative_base()

db_user = environ.get("DB_USER", "root")
db_pass = environ.get("DB_PASS", "")
db_host = environ.get("DB_HOST", "localhost")
db_name = environ.get("DB_NAME", "flask_app")


# DATABASE_URL = f"mysql://{db_user}:{db_pass}@{db_host}/{db_name}"
DATABASE_URL = "sqlite:///dev_database.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
