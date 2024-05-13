from config.db import engine, meta
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String


patients = Table(
    'patients', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('mobile', String(10)),
    Column('address', String(255))
)
