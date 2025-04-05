from flask_sqlalchemy import SQLAlchemy
from src.database.db import db

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_reason = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return f'<LeaveRequest {self.leave_type} {self.status}>'