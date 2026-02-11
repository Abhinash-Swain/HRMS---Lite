from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud
from database import SessionLocal, engine, get_db
from datetime import date

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="Backend API for HRMS Lite application",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
    "https://your-frontend-deployment-url.vercel.app" # Placeholder for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for simplicity in this assignment, restrict in real prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to HRMS Lite API"}

@app.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)

# --- Employee Endpoints ---

@app.post("/employees/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_employee_id = crud.get_employee_by_emp_id(db, emp_id=employee.employee_id)
    if db_employee_id:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    return crud.create_employee(db=db, employee=employee)

@app.get("/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.delete("/employees/{employee_id}", response_model=schemas.Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# --- Attendance Endpoints ---

@app.post("/attendance/", response_model=schemas.Attendance)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    # Verify employee exists
    db_employee = crud.get_employee(db, employee_id=attendance.employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return crud.create_attendance(db=db, attendance=attendance)

@app.get("/attendance/", response_model=List[schemas.Attendance])
def read_attendance(skip: int = 0, limit: int = 100, date: Optional[date] = None, db: Session = Depends(get_db)):
    attendance_records = crud.get_attendance(db, skip=skip, limit=limit, date_filter=date)
    return attendance_records

@app.get("/attendance/{employee_id}", response_model=List[schemas.Attendance])
def read_attendance_by_employee(employee_id: int, db: Session = Depends(get_db)):
     # Verify employee exists
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return crud.get_attendance_by_employee(db, employee_id=employee_id)
