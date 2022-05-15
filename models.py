from __future__ import annotations
from . import db
from flask_login import UserMixin
from dataclasses import dataclass

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
class TestRecord(db.Model):
    id: int
    visitor_id: int
    is_positive: bool
    time_tested: db.DateTime
    timestamp: db.DateTime

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    visitor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_positive = db.Column(db.Boolean)
    time_tested = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime)

@dataclass
class ExposureStatus(db.Model):
    id: int
    visitor_id: int
    business_id: str
    status: str
    time_exposed: db.DateTime
    timestamp: db.DateTime

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    visitor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    status = db.Column(db.String(10))
    time_exposed = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime)

@dataclass
class Location(db.Model):
    address1: str
    address2: str
    city: str
    zipcode: int
    country: str
    state: str

    id = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String(80))
    address2 = db.Column(db.String(80))
    city = db.Column(db.String(20))
    country = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zipcode = db.Column(db.Integer)

@dataclass
class Business(db.Model):
    id: int
    owner_id: int
    latitude: float
    longitude: float
    name: str
    location_id: int
    location: Location
    category: str
    visit_records: list[VisitRecord]

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(1000), unique=True)
    category = db.Column(db.String(20))
    visit_records = db.relationship("VisitRecord")
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", uselist=False)

@dataclass
class User(UserMixin, db.Model):
    id: int
    email: str
    password: str
    name: str
    businesses: list[Business]
    visit_records: list[VisitRecord]
    # test_records: list[TestRecord]
    # exposures: list[ExposureStatus]

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    businesses = db.relationship("Business")
    visit_records = db.relationship("VisitRecord")
    # test_records = db.relationship("TestRecord")
    # exposures = db.relationship("ExposureStatus")
