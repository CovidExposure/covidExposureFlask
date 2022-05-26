from flask import request, Blueprint, jsonify
from flask_login import current_user
from . import db
from .models import TestRecord, VisitRecord
from datetime import datetime, timedelta

visitor = Blueprint('visitor', __name__)

@visitor.route('/visitor/test_record')
def getTestRecords():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

    visitor_id = current_user.get_id()
    records = TestRecord.query.filter_by(visitor_id=visitor_id).all()

    # TODO(Duo Wang): pagination of records
    return jsonify({"success": True, "content": records})

@visitor.route('/visitor/test_record', methods=['POST'])
def uploadTestRecord():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

    visitor_id = int(current_user.get_id())
    is_positive = request.form.get('isPositive') == "true" or request.form.get('isPositive') == "True"
    time_tested = datetime.fromisoformat(request.form.get('timeTested'))
    timestamp = datetime.now()

    new_test_record = TestRecord(visitor_id=visitor_id,is_positive=is_positive,time_tested=time_tested,timestamp=timestamp)
    db.session.add(new_test_record)
    db.session.commit()

    if is_positive:
        handleExposure(visitor_id,time_tested)

    return jsonify({"success": True, "content": new_test_record}), 201

def handleExposure(visitor_id,time_tested):
    records = VisitRecord.query.with_entities(VisitRecord.business_id, VisitRecord.timestamp).filter(VisitRecord.timestamp > time_tested-timedelta(days=7), VisitRecord.timestamp < time_tested+timedelta(days=7), VisitRecord.visitor_id == visitor_id).all()
    VisitRecord.query.filter(VisitRecord.timestamp > time_tested-timedelta(days=7), VisitRecord.timestamp < time_tested+timedelta(days=7), VisitRecord.visitor_id == visitor_id).update({"status":"POSITIVE"})
    for business_id, time_visited in records:
        VisitRecord.query.filter(VisitRecord.timestamp >= time_visited-timedelta(hours=3), VisitRecord.timestamp <= time_visited+timedelta(hours=3), VisitRecord.business_id == business_id, VisitRecord.status != "POSITIVE").update({"status":"EXPOSED"})
    db.session.commit()

@visitor.route('/visitor/visit_records')
def getVisitRecord():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "failure": "Please login"}), 403

    visitor_id = current_user.get_id()
    visits =  VisitRecord.query.filter_by(visitor_id=visitor_id).all()

    # TODO(Duo Wang): pagination of visits
    return jsonify({"success": True, "content": visits})

