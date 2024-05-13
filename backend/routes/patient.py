from fastapi import APIRouter
from config.db import conn
from models.index import patients
from schemas.index import Patient
from sqlalchemy.sql import select, insert
from math import ceil
patient = APIRouter()


@patient.get('/')
async def read_data(page: int = 1, limit: int = None, search: str = None):
    stmt = select(patients)
    total_rec = conn.execute(stmt).mappings().all()
    total_page = ceil(len(total_rec) / limit) if limit else 1
    
    if search:
        stmt = stmt.where(patients.c.name.ilike(f"%{search}%"))
    
    if limit:
        stmt = stmt.limit(limit).offset((page - 1) * limit)
    
    return {"result": conn.execute(stmt).mappings().all(), "totalPages": total_page}


@patient.get('/{id}')
async def read_single_data(id: int):
    stmt = select(patients).where(patients.c.id == id)
    return conn.execute(stmt).mappings().all()


@patient.post('/')
async def write_data(patient_data: Patient):
    stmt = insert(patients).values(
        name=patient_data.name,
        email=patient_data.email,
        mobile=patient_data.mobile,
        address=patient_data.address
    )
    conn.execute(stmt)
    conn.commit()

    return conn.execute(select(patients)).mappings().all()



# @patient.put('/{id}')
# async def update_data(id: int, user: User):
#     stmt = update(users).where(users.c.id == id).values(
#         name=user.name,
#         email=user.email,
#         password=user.password
#     )

#     conn.execute(stmt)
#     conn.commit()
#     return conn.execute(select(users).where(users.c.id == id)).mappings().all()


# @user.delete('/{id}')
# async def delete_data(id: int):
#     stmt = delete(users).where(users.c.id == id)
#     conn.execute(stmt)
#     conn.commit()
#     return conn.execute(select(users)).mappings().all()
