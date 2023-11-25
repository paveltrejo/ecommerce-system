import os

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())
user = os.getenv("DB_USER", "")
password = os.getenv("DB_PASS", "")
host = os.getenv("DB_HOST", "")
port = os.getenv("DB_PORT", "")
db = os.getenv("DB_NAME", "")
mongo_db = os.getenv("MONGO_DB_NAME", "")
mongo_collection = os.getenv("MONGO_COLLECT", "")

print(f"user {user}")
print(f"password {password}")
print(f"host {host}")
print(f"port {port}")
print(f"db {db}")


#Configuracion para la base de datos Postgresql
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
#SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Configuracion para la base de datos mongodb
mongo_client = MongoClient('mongodb://localhost:27017')
mongo_db = mongo_client[str({mongo_db})]
collection = mongo_db[str({mongo_collection})]

Base = declarative_base()


def db_mapping_rows_to_dict(query):
    """Convierte una consulta  sqlalchemy.engine.row.Row a un diccionario"""
    result = []
    for row in query:
        result.append(row._mapping)
    return result
