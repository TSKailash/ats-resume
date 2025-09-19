from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import mongo
import datetime

hr_bp=Blueprint("hr", __name__)

@hr_bp.route("/profile", methods=["POST"])
def get_hr_profile():
    body=request.get_json()
    email=body.get("email")
    # print("Request JSON:", body)
    hr=mongo.db.hr_profiles.find_one({"email": email})

    if not hr:
        return jsonify({"msg": "HR Profile not found"}), 404
    
    hr["_id"]=str(hr["_id"])
    del hr["password"]
    return jsonify(hr), 200

