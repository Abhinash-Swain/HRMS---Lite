from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from datetime import date

# --- Employee CRUD ---
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employee_by_emp_id(db: Session, emp_id: str):
    return db.query(models.Employee).filter(models.Employee.employee_id == emp_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee

# --- Attendance CRUD ---
def get_attendance(db: Session, skip: int = 0, limit: int = 100, date_filter: date = None):
    query = db.query(models.Attendance)
    if date_filter:
        query = query.filter(models.Attendance.date == date_filter)
    return query.offset(skip).limit(limit).all()

def get_attendance_by_employee(db: Session, employee_id: int):
    return db.query(models.Attendance).filter(models.Attendance.employee_id == employee_id).all()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    # Check if attendance already exists for this employee on this date
    existing_attendance = db.query(models.Attendance).filter(
        models.Attendance.employee_id == attendance.employee_id,
        models.Attendance.date == attendance.date
    ).first()
    
    if existing_attendance:
        # Update existing record
        existing_attendance.status = attendance.status
        db.commit()
        db.refresh(existing_attendance)
        return existing_attendance
        
    db_attendance = models.Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_dashboard_stats(db: Session):
    today = date.today()
    
    total_employees = db.query(models.Employee).count()
    
    present_today = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == 'Present'
    ).count()
    
    absent_today = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == 'Absent'
    ).count()
    
    leave_today = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == 'Leave'
    ).count()
    
    return {
        "total_employees": total_employees,
        "present_today": present_today,
        "absent_today": absent_today,
        "leave_today": leave_today
    }
