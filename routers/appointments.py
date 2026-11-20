from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import SessionDep
from models.models import Appointment, Doctor, Patient
from schemas.schemas import AppointmentUpdate

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# Create Appointment
@router.post("/")
def create_appointment(appointment: Appointment, session: SessionDep):

    doctor = session.get(Doctor, appointment.doctor_id)
    patient = session.get(Patient, appointment.patient_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


# Get All Appointments
@router.get("/")
def get_appointments(session: SessionDep):
    appointments = session.exec(select(Appointment)).all()
    return appointments


# Get Single Appointment
@router.get("/{appointment_id}")
def get_appointment(appointment_id: int, session: SessionDep):
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


# Update Appointment
@router.patch("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    session: SessionDep
):
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = data.model_dump(exclude_unset=True)

    if "doctor_id" in update_data:
        if not session.get(Doctor, update_data["doctor_id"]):
            raise HTTPException(status_code=404, detail="Doctor not found")

    if "patient_id" in update_data:
        if not session.get(Patient, update_data["patient_id"]):
            raise HTTPException(status_code=404, detail="Patient not found")

    appointment.sqlmodel_update(update_data)

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


# Delete Appointment
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, session: SessionDep):
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    session.delete(appointment)
    session.commit()

    return {"message": "Appointment deleted successfully"}
