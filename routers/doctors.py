from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import SessionDep
from models.models import Doctor
from schemas.schemas import DoctorUpdate

router = APIRouter(prefix="/doctors",tags=["Doctors"])


@router.post("/")
def create_doctor(doctor: Doctor, session: SessionDep):
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


@router.get("/")
def get_doctors(session: SessionDep):
    doctors = session.exec(select(Doctor)).all()
    return doctors


@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, session: SessionDep):
    doctor = session.get(Doctor, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


@router.patch("/{doctor_id}")
def update_doctor(doctor_id: int, data: DoctorUpdate, session: SessionDep):
    doctor = session.get(Doctor, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.sqlmodel_update(data.model_dump(exclude_unset=True))

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, session: SessionDep):
    doctor = session.get(Doctor, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    session.delete(doctor)
    session.commit()

    return {"message": "Doctor deleted successfully"}
