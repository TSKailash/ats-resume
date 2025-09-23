from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from extensions import mongo
import datetime
from bson.objectid import ObjectId

job_bp = Blueprint("job", __name__)

@job_bp.route("/post-job", methods=["POST"])
@jwt_required()
def create_job():
    hr_id = get_jwt_identity() 
    hr = mongo.db.hr_profiles.find_one({"_id": ObjectId(hr_id)})

    if not hr:
        return jsonify({"msg": "HR profile not found"}), 404

    data = request.get_json()
    required_fields = ["title", "description", "location", "salary", "requirements", "experience_level"]

    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    if not isinstance(data["requirements"], list) or not all(isinstance(r, str) for r in data["requirements"]):
        return jsonify({"msg": "requirements must be a list of strings"}), 400

    job = {
        "title": data["title"],
        "description": data["description"],
        "location": data["location"],
        "salary": data["salary"],
        "requirements": data["requirements"],  
        "experience_level": data["experience_level"],
        "company_name": hr["company_name"],     
        "hr_id": hr_id,                         
        "created_at": datetime.utcnow(),
        "status": "open",
        "applications": []
    }

    result = mongo.db.jobs.insert_one(job)
    job["_id"] = str(result.inserted_id)

    return jsonify({
        "msg": "Job created successfully",
        "job": job
    }), 201

@job_bp.route("/get-jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    hr_id=get_jwt_identity()
    jobs = list(mongo.db.jobs.find({"hr_id": hr_id}))  

    for job in jobs:
        job["_id"] = str(job["_id"])
        job["hr_id"] = str(job["hr_id"])

    return jsonify(jobs), 200

@job_bp.route("/update-job/<job_id>", methods=["POST"])
@jwt_required()
def update_job(job_id):
    hr_id = get_jwt_identity()
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id), "hr_id": hr_id})

    if not job:
        return jsonify({"msg": "Job not found or unauthorized"}), 404

    data = request.get_json()
    update_fields = {}

    allowed_fields = ["title", "description", "location", "salary", "requirements", "experience_level", "status"]

    for field in allowed_fields:
        if field in data:
            if field == "requirements":
                if not isinstance(data["requirements"], list) or not all(isinstance(r, str) for r in data["requirements"]):
                    return jsonify({"msg": "requirements must be a list of strings"}), 400
            update_fields[field] = data[field]

    if not update_fields:
        return jsonify({"msg": "No valid fields to update"}), 400

    mongo.db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": update_fields})
    updated_job = mongo.db.jobs.find_one({"_id": ObjectId(job_id)})

    updated_job["_id"] = str(updated_job["_id"])
    updated_job["hr_id"] = str(updated_job["hr_id"])

    return jsonify({
        "msg": "Job updated successfully",
        "job": updated_job
    }), 200

@job_bp.route("/delete-job/<job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    hr_id = get_jwt_identity()
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id), "hr_id": hr_id})

    if not job:
        return jsonify({"msg": "Job not found or unauthorized"}), 404

    mongo.db.jobs.delete_one({"_id": ObjectId(job_id)})

    return jsonify({"msg": "Job deleted successfully"}), 200

@job_bp.route("/get-applications/<job-id>", methods=["GET"])
@jwt_required()
def get_applications(job_id):
    hr_id = get_jwt_identity()
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id), "hr_id": hr_id})

    if not job:
        return jsonify({"msg": "Job not found"}), 404
    
    applications=job.get("applications", [])
    detailed_applications = []
    for app in applications:
        candidate = mongo.db.candidate_profiles.find_one({"_id": ObjectId(app["candidate_id"])})
        if candidate:
            candidate["_id"] = str(candidate["_id"])
            detailed_applications.append({
                "application_id": str(app["_id"]),
                "candidate": candidate,
                "status": app["status"],
                "applied_at": app["applied_at"]
            })

    return jsonify(detailed_applications), 200

