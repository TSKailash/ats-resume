from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import mongo
import datetime
from bson.objectid import ObjectId


admin_bp=Blueprint("admin", __name__)

@admin_bp.route("/requests", methods=["GET"])
def get_requests():
    requests=list(mongo.db.hr_requests.find({"req_status": "pending"}))
    for r in requests:
        r["_id"]=str(r["_id"])

    return jsonify(requests), 200

@admin_bp.route("/requests/<request_id>/approve", methods=["POST"])
def approve_hr_req(request_id):
    hr_req=mongo.db.hr_requests.find_one({"_id": ObjectId(request_id)})

    if not hr_req:
        return jsonify({"msg": "Request not found"}), 404
    
    if hr_req["req_status"] != "pending":
        return jsonify({"msg": "Request already reviewed"}), 400
    
    mongo.db.hr_profiles.insert_one({
        "username": hr_req["username"],
        "email": hr_req["email"],
        "password": hr_req["password"], 
        "p_no": hr_req["p_no"],
        "role": hr_req["role"],
        "company_name": hr_req["company_name"],
        "cin_number": hr_req["cin_number"],
        "created_at": datetime.datetime.utcnow()
    })

    mongo.db.hr_requests.update_one({"_id": hr_req["_id"]}, {"$set": {"req_status": "approved"}})

    return jsonify({"msg": "HR approved successfully"}), 200

@admin_bp.route("/requests/<request_id>/reject", methods=["DELETE"])
def reject_hr_req(request_id):
    hr_req = mongo.db.hr_requests.find_one({"_id": ObjectId(request_id)})

    if not hr_req:
        return jsonify({"msg": "Request not found"}), 404

    if hr_req["req_status"] != "pending":
        return jsonify({"msg": "Request already reviewed"}), 400

    mongo.db.hr_requests.update_one({"_id": hr_req["_id"]}, {"$set": {"req_status": "rejected"}})

    return jsonify({"msg": "HR request rejected"}), 200