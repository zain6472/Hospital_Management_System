from datetime import datetime
from sqlmodel import SQLModel

class DoctorUpdate(SQLModel):
    name: str | None = None
    age: int | None = None

class PatientUpdate(SQLModel):
    name: str | None = None
    phone: str | None = None
    age: int | None = None

class AppointmentUpdate(SQLModel):
    doctor_id: int | None = None
    patient_id: int | None = None
    appointment_date: datetime | None = None
    reason: str | None = None

class BillUpdate(SQLModel):
    appointment_id: int | None = None
    amount: float | None = None

from sqlmodel import SQLModel


class PharmacyUpdate(SQLModel):
    medicine_name: str | None = None
    price: float | None = None
    quantity: int | None = None


class LaboratoryUpdate(SQLModel):
    patient_id: int | None = None
    test_name: str | None = None
    test_date: str | None = None
    result: str | None = None
