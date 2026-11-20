from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import SessionDep
from models.models import Bill, Appointment
from schemas.schemas import BillUpdate

router = APIRouter(prefix="/bills",tags=["Bills"])


@router.post("/")
def create_bill(bill: Bill, session: SessionDep):

    appointment = session.get(Appointment, bill.appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    session.add(bill)
    session.commit()
    session.refresh(bill)

    return bill


@router.get("/")
def get_bills(session: SessionDep):
    bills = session.exec(select(Bill)).all()
    return bills


@router.get("/{bill_id}")
def get_bill(bill_id: int, session: SessionDep):
    bill = session.get(Bill, bill_id)

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    return bill


@router.patch("/{bill_id}")
def update_bill(bill_id: int, data: BillUpdate, session: SessionDep):
    bill = session.get(Bill, bill_id)

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    update_data = data.model_dump(exclude_unset=True)

    if "appointment_id" in update_data:
        appointment = session.get(Appointment, update_data["appointment_id"])

        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

    bill.sqlmodel_update(update_data)

    session.add(bill)
    session.commit()
    session.refresh(bill)

    return bill


@router.delete("/{bill_id}")
def delete_bill(bill_id: int, session: SessionDep):
    bill = session.get(Bill, bill_id)

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    session.delete(bill)
    session.commit()

    return {"message": "Bill deleted successfully"}
