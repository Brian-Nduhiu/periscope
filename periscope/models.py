from datetime import timezone
from enum import unique

from periscope.views import activity
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    # shift = db.relationship('Shift')


class Supervisor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

# class Shift(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     sites = db.Column(db.String(100000))
#     activity = db.Column(db.Integer)