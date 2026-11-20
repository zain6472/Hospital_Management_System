from fastapi import FastAPI
from database import create_db_and_tables
from routers import doctors, patients, appointments, bills ,pharmacy, laboratory

app = FastAPI(title="Hospital Management System")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "Welcome to Hospital Management System"}

app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(bills.router)
app.include_router(pharmacy.router)
app.include_router(laboratory.router)