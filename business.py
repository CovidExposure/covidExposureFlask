from flask import request, Blueprint, jsonify
from flask_login import current_user
from .models import Business, VisitRecord, Location
from . import db
from datetime import datetime
from .googlemap import searchPlaceID, getPlaceCoords


business = Blueprint('business', __name__)


@business.route('/business')
def listBusinesses():
    if not current_user.is_authenticated:
        return "please login", 403

    owner_id = current_user.get_id()

    businesses = Business.query.filter_by(owner_id=owner_id).all()

    # TODO(Duo Wang): pagination of visit_records
    return jsonify(businesses), 200


@business.route('/business', methods=['POST'])
def createBusiness():
    if not current_user.is_authenticated:
        return "please login", 403
    
    name = request.form.get('name')
    # category = request.form.get('category')
    zipcode = int(request.form.get('zipcode'))
    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    country = request.form.get('country')
    city = request.form.get('city')
    state = request.form.get('state')
    owner_id = current_user.get_id()

    coords = getPlaceCoords(searchPlaceID(" ".join([address1,city,state,country])))
    latitude = coords['lat']
    longitude = coords['lng']

    business = Business.query.filter_by(name=name).first()

    if business:
        return "business name already taken", 304

    new_location = Location(address1=address1,address2=address2,country=country,state=state,zipcode=zipcode,city=city,latitude=latitude,longitude=longitude)
    db.session.add(new_location)
    new_business = Business(location=new_location,name=name,owner_id=owner_id)
    db.session.add(new_business)
    db.session.commit()
    
    return getBusinessCheckInLink(new_business.id)


def getBusinessCheckInLink(business_id):
    return "/business/{business_id}/checkin"


@business.route('/business/<business_id>/checkin')
def checkin(business_id):
    if not current_user.is_authenticated:
        return "please login", 403

    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return "business not found", 404

    visitor_id = current_user.get_id()
    timestamp = datetime.now()
    new_visit_record = VisitRecord(business_id=business_id,visitor_id=visitor_id,timestamp=timestamp)
    db.session.add(new_visit_record)
    db.session.commit()

    return jsonify(new_visit_record), 200