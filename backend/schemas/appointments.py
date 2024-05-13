from pydantic import BaseModel
from datetime import datetime


class Appointment(BaseModel):
    patient_id: int
    patient_name: str
    date_time: datetime
    notes: str
    payment_status: str

    class Config:
        orm_mode = True
