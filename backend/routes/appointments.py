from fastapi import APIRouter, HTTPException
from config.db import conn
from models.index import appointments, patients
from schemas.index import Appointment, Patient
from sqlalchemy.sql import select, insert

appointment = APIRouter()


@appointment.get('/{patient_id}')
async def get_patient_with_appointments(patient_id: int):
    # Fetch patient details
    patient_stmt = select(patients).where(patients.c.id == patient_id)
    patient_result = conn.execute(patient_stmt).first()
    
    if not patient_result:
        raise HTTPException(status_code=404, detail=f"No patient found with ID {patient_id}")

    # Convert patient result to a dictionary
    patient_data = dict(patient_result._asdict())
    
    # Fetch appointments for the patient
    appointment_stmt = select(appointments).where(appointments.c.patient_id == patient_id)
    appointment_results = conn.execute(appointment_stmt).all()

    # Convert appointment results to a list of dictionaries
    appointments_data = [dict(zip(appointments.c.keys(), appointment)) for appointment in appointment_results]

    # Add appointments data to patient data
    patient_data['appointments'] = appointments_data

    return patient_data


@appointment.post('/')
async def create_appointment(appointment_data: Appointment):
    try:
        stmt = insert(appointments).values(
            patient_id=appointment_data.patient_id,
            patient_name=appointment_data.patient_name,
            date_time=appointment_data.date_time,
            notes=appointment_data.notes,
            payment_status=appointment_data.payment_status
        )
        conn.execute(stmt)
        conn.commit()
        return {"message": "Appointment created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create appointment: {str(e)}")
