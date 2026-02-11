from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum

class AttendanceStatusEnum(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"

# --- Employee Schemas ---
class EmployeeBase(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str
    designation: Optional[str] = None
    joined_date: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

# --- Attendance Schemas ---
class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatusEnum # Use Enum for validation

class AttendanceCreate(AttendanceBase):
    employee_id: int

class Attendance(AttendanceBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True

class AttendanceOut(Attendance):
     employee: Optional[Employee] = None

class DashboardStats(BaseModel):
    total_employees: int
    present_today: int
    absent_today: int
    leave_today: int
