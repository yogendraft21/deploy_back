from config.db import meta
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

appointments = Table(
    'appointments', meta,
    Column('id', Integer, primary_key=True),
    Column('patient_id', Integer, ForeignKey('patients.id')),
    Column('patient_name', String(255)),
    Column('date_time', DateTime),
    Column('notes', String(255)),
    Column('payment_status', String(50))
)
