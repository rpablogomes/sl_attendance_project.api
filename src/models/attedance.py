from src.db import db
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return f'<Attendance {self.date} - {self.status}>'