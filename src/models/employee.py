from src.db import db
import bcrypt
from flask_login import UserMixin

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) 
    family_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    leaves = db.relationship('LeaveRequest', backref='employee', lazy=True)
    attendance = db.relationship('Attendance', backref='employee', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'family_name': self.family_name
        }

    def __repr__(self):
        return f'<Employee {self.name}>'
