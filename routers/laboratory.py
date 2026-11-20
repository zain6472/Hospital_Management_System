
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from database import SessionDep
from models.models import Laboratory, Patient
from schemas.schemas import LaboratoryUpdate

router = APIRouter(prefix="/laboratory", tags=["Laboratory"])


@router.post("/")
def add_test(data: Laboratory, session: SessionDep):
    patient = session.get(Patient, data.patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@router.get("/")
def get_tests(session: SessionDep):
    return session.exec(select(Laboratory)).all()


@router.get("/{test_id}")
def get_test(test_id: int, session: SessionDep):
    test = session.get(Laboratory, test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    return test


@router.patch("/{test_id}")
def update_test(
    test_id: int,
    data: LaboratoryUpdate,
    session: SessionDep
):
    test = session.get(Laboratory, test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    update_data = data.model_dump(exclude_unset=True)

    if "patient_id" in update_data:
        patient = session.get(Patient, update_data["patient_id"])

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

    test.sqlmodel_update(update_data)

    session.add(test)
    session.commit()
    session.refresh(test)

    return test


@router.delete("/{test_id}")
def delete_test(test_id: int, session: SessionDep):
    test = session.get(Laboratory, test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    session.delete(test)
    session.commit()

    return {"message": "Test deleted successfully"}
