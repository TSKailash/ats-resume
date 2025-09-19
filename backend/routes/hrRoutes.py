from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import mongo
from bson.objectid import ObjectId
import datetime

hr_bp=Blueprint("hr", __name__)

@hr_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_hr_profile():
    body=get_jwt_identity()
    user=mongo.db.hr_profiles.find_one({"_id": ObjectId(body)})
    email=user["email"]
    # print("Request JSON:", body)
    hr=mongo.db.hr_profiles.find_one({"email": email})

    if not hr:
        return jsonify({"msg": "HR Profile not found"}), 404
    
    hr["_id"]=str(hr["_id"])
    del hr["password"]
    return jsonify(hr), 200

@hr_bp.route("/profile/update", methods=["PUT"])
@jwt_required()
def update_hr_profile():
    current=get_jwt_identity()
    data=request.get_json() #Get new username, new phone-no(or exixting), new Company and its CIN number and password for verification

    user=mongo.db.hr_profiles.find_one({"_id": ObjectId(current)})
    print(jsonify(user))

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not check_password_hash(user["password"], data.get("password")):
        return jsonify({"msg": "Incorrect password"}), 401

    allowed=["username", "p_no", "company_name", "cin_number"]

    update_data={field: data[field] for field in allowed if field in data}

    if "p_no" in update_data:
        if not update_data["p_no"].isdigit() or len(update_data["p_no"]) != 10:
            return jsonify({"msg": "Invalid phone number"}), 400
        
    if not update_data:
        return jsonify({"msg": "No valid fields to update"}), 400
    
    mongo.db.hr_profiles.update_one({
        "_id": ObjectId(current)
    }, {
        "$set": update_data
    })

    return jsonify({"msg": "Profile updated successfully"}), 200
