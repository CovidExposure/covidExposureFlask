import json
from flask import request, Blueprint, jsonify
from flask_login import current_user
from .models import Business, VisitRecord
from . import db
from datetime import datetime


business = Blueprint('business', __name__)


@business.route('/business')
def listBusinesses():
    if not current_user.is_authenticated:
        return "please login", 403
    # TODO(Duo Wang): refine with Google Map API

    owner_id = current_user.get_id()

    businesses = Business.query.filter_by(owner_id=owner_id).all()

    # TODO(Duo Wang): pagination of visit_records
    return jsonify(businesses), 200


@business.route('/business', methods=['POST'])
def createBusiness():
    if not current_user.is_authenticated:
        return "please login", 403
    # TODO(Duo Wang): refine with Google Map API

    county = request.form.get('county')
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    name = request.form.get('name')
    state = request.form.get('state')
    type = request.form.get('type')
    zipcode = int(request.form.get('zipcode'))
    owner_id = current_user.get_id()


    business = Business.query.filter_by(name=name).first()

    if business:
        return "business name already taken", 304

    new_business = Business(county=county,latitude=latitude,longitude=longitude,name=name,state=state,type=type,owner_id=owner_id,zipcode=zipcode)
    db.session.add(new_business)
    db.session.commit()
    
    return getBusinessCheckInLink(new_business.id)


def getBusinessCheckInLink(business_id):
    return "/business/{business_id}/checkin"


@business.route('/business/<business_id>/checkin', methods=['GET'])
def checkin_post(business_id):
    if not current_user.is_authenticated:
        return "please login", 403

    visitor_id = current_user.get_id()
    timestamp = datetime.now()
    new_visit_record = VisitRecord(business_id=business_id,visitor_id=visitor_id,timestamp=timestamp)
    db.session.add(new_visit_record)
    db.session.commit()

    return jsonify(new_visit_record), 200