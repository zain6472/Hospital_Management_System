
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from database import SessionDep
from models.models import Pharmacy
from schemas.schemas import PharmacyUpdate

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@router.post("/")
def add_medicine(data: Pharmacy, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@router.get("/")
def get_medicines(session: SessionDep):
    return session.exec(select(Pharmacy)).all()


@router.get("/{medicine_id}")
def get_medicine(medicine_id: int, session: SessionDep):
    medicine = session.get(Pharmacy, medicine_id)

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    return medicine


@router.patch("/{medicine_id}")
def update_medicine(
    medicine_id: int,
    data: PharmacyUpdate,
    session: SessionDep
):
    medicine = session.get(Pharmacy, medicine_id)

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    medicine.sqlmodel_update(data.model_dump(exclude_unset=True))

    session.add(medicine)
    session.commit()
    session.refresh(medicine)

    return medicine


@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, session: SessionDep):
    medicine = session.get(Pharmacy, medicine_id)

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    session.delete(medicine)
    session.commit()

    return {"message": "Medicine deleted successfully"}
