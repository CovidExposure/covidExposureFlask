from . import db
from flask_login import UserMixin
from dataclasses import dataclass
# from sqlalchemy.orm import relationship

@dataclass
class VisitRecord(db.Model):
    id: int
    visitor_id: int
    business_id: str
    timestamp: db.DateTime

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    visitor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    timestamp = db.Column(db.DateTime)

@dataclass
class Business(db.Model):
    id: int
    owner_id: int
    county: str
    latitude: float
    longitude: float
    name: str
    state: str
    type: str
    zipcode: int
    visit_records: list[VisitRecord]

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    county = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(1000), unique=True)
    state = db.Column(db.String(20))
    type = db.Column(db.String(20))
    zipcode = db.Column(db.Integer)
    visit_records = db.relationship("VisitRecord")

@dataclass
class User(UserMixin, db.Model):
    id: int
    email: str
    password: str
    name: str
    businesses: list[Business]
    visit_records: list[VisitRecord]

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    businesses = db.relationship("Business")
    visit_records = db.relationship("VisitRecord")

