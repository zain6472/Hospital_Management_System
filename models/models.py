from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Doctor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    appointments: list["Appointment"] = Relationship(back_populates="doctor")


class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    age: int
    appointments: list["Appointment"] = Relationship(back_populates="patient")


class Appointment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.id")
    patient_id: int = Field(foreign_key="patient.id")
    appointment_date: datetime
    reason: str

    doctor: Doctor | None = Relationship(back_populates="appointments")
    patient: Patient | None = Relationship(back_populates="appointments")
    bills: list["Bill"] = Relationship(back_populates="appointment")


class Bill(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    appointment_id: int = Field(foreign_key="appointment.id")
    amount: float
    appointment: Appointment | None = Relationship(back_populates="bills")


from sqlmodel import SQLModel, Field


class Pharmacy(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    medicine_name: str
    price: float
    quantity: int


class Laboratory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    test_name: str
    test_date: str
    result: str | None = None
