from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import SessionDep
from models.models import Patient
from schemas.schemas import PatientUpdate

router = APIRouter(prefix="/patients",tags=["Patients"])


@router.post("/")
def create_patient(patient: Patient, session: SessionDep):
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.get("/")
def get_patients(session: SessionDep):
    patients = session.exec(select(Patient)).all()
    return patients


@router.get("/{patient_id}")
def get_patient(patient_id: int, session: SessionDep):
    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@router.patch("/{patient_id}")
def update_patient(patient_id: int, data: PatientUpdate, session: SessionDep):
    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.sqlmodel_update(data.model_dump(exclude_unset=True))

    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, session: SessionDep):
    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    session.delete(patient)
    session.commit()
    return {"message": "Patient deleted successfully"}