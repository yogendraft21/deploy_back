from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()
meta = MetaData()
db_url = os.getenv("DB_URL")

engine = create_engine(db_url)

conn = engine.connect()
