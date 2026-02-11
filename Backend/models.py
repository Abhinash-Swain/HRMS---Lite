from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import date

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    designation = Column(String, nullable=True)
    joined_date = Column(Date, default=date.today)

    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")


class AttendanceStatus(str, enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, default=date.today, nullable=False)
    status = Column(String, nullable=False) # Storing as string to keep it simple with SQLite/Postgres compatibility

    employee = relationship("Employee", back_populates="attendance_records")
