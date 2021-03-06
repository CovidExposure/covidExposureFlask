from flask import request, Blueprint, jsonify, current_app
from flask_login import current_user
from pyzbar.pyzbar import decode
from PIL import Image
import os
from werkzeug.utils import secure_filename
from .models import Business, VisitRecord, Location, TestRecord
from . import db
from datetime import datetime, timedelta
from .googlemap import searchPlaceID, getPlaceCoords


business = Blueprint('business', __name__)


@business.route('/business')
def listBusinesses():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

    owner_id = current_user.get_id()

    businesses = Business.query.filter_by(owner_id=owner_id).all()

    # TODO(Duo Wang): pagination of visit_records
    return jsonify({"success": True, "content": businesses})


@business.route('/business', methods=['POST'])
def createBusiness():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

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
        return jsonify({"success": False, "failure": "Business name already taken"}), 304

    new_location = Location(address1=address1,address2=address2,country=country,state=state,zipcode=zipcode,city=city,latitude=latitude,longitude=longitude)
    db.session.add(new_location)
    new_business = Business(location=new_location,name=name,owner_id=owner_id)
    db.session.add(new_business)
    db.session.commit()
    
    return jsonify({"success": True, "content": getBusinessCheckInLink(new_business.id)}), 201


def getBusinessCheckInLink(business_id):
    return f"/business/{business_id}/checkin"


@business.route('/business/qr-code', methods=['POST'])
def decode_qr():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

    target = os.path.join(current_app.config['UPLOAD_FOLDER'])
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    file.save("/".join([target, filename]))
    dataList = decode(Image.open("/".join([target, filename])))
    checkin_link = str(dataList[0].data.decode('ascii'))

    return jsonify({"success": True, "content": checkin_link})


@business.route('/business/<business_id>/checkin', methods=['POST'])
def checkin(business_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({"success": False, "failure": "Business not found"}), 404

    visitor_id = current_user.get_id()
    timestamp = datetime.now()
    latest_test_record = TestRecord.query.filter_by(visitor_id=visitor_id).order_by(TestRecord.time_tested.desc()).first()
    status = "POSITIVE" if latest_test_record and latest_test_record.is_positive and latest_test_record.time_tested > timestamp-timedelta(days=7) else "NOT EXPOSED"
    new_visit_record = VisitRecord(business_id=business_id,visitor_id=visitor_id,status=status,timestamp=timestamp)
    db.session.add(new_visit_record)
    db.session.commit()

    return jsonify({"success": True, "content": new_visit_record}), 201
