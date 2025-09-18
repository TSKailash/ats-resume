from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import mongo
import datetime


auth_bp=Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data=request.get_json()
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    confirm_password=data.get("confirm_password")
    p_no=data.get("p_no")
    role=data.get("role")

    if password!=confirm_password:
        return jsonify({"msg": "Passwords do not match"}), 400
    
    p_no = str(data.get("p_no"))

    if not p_no.isdigit() or len(p_no) != 10:
        return jsonify({"msg": "Invalid phone number"}), 400
    
    if mongo.db.users.find_one({"email": email}) or mongo.db.hr_profiles.find_one({"email": email}):
        return jsonify({"msg": "Email already exists"}), 400

    hashed=generate_password_hash(password)

    if role=="hr":
        company_name=data.get("company_name")
        cin_number=data.get("cin_number")
        if not all ([username, email, password, confirm_password, p_no, role, company_name, cin_number]):
            return jsonify({"msg": "All fields are required"}), 400
        
        if mongo.db.hr_profiles.find_one({"email":email}):
            return jsonify({"msg": "User already exists"}), 400
        

        if mongo.db.hr_requests.find_one({"email":email}):
            hr=mongo.db.hr_requests.find_one({"email":email})
            if hr["req_status"]!="pending":
                return jsonify({"msg":"Account already reviewed. Please try to login"}), 400
            else:
                return jsonify({"msg": "Account under verification"}), 400
            
        mongo.db.hr_requests.insert_one({
            "username":username,
            "email":email,
            "password":hashed,
            "p_no": p_no,
            "role":role,
            "company_name": company_name,
            "cin_number": cin_number,
            "req_status": "pending"
        })
        
        return jsonify({"msg": "Request sent successfully. Please wait for admin approval"}), 201


    if not all ([username, email, password, confirm_password, role]):
        return jsonify({"msg": "All fields are required"}), 400
    
    if mongo.db.users.find_one({"email":email}):
        return jsonify({"msg": "User already exists"}), 400
    
    hashed=generate_password_hash(password)

    mongo.db.users.insert_one({
        "username":username,
        "email":email,
        "password":hashed,
        "p_no": p_no,
        "role":role
    })

    return jsonify({"msg": "success"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    user=mongo.db.users.find_one({"email": email})
    hr=mongo.db.hr_profiles.find_one({"email": email})

    if not user and not hr:
        return jsonify({"msg": "User Not Found"}), 401
    
    if user:
        if not check_password_hash(user["password"], password):
            return jsonify({"msg": "Invalid Credentials"}), 401
        
        access_token=create_access_token(identity=str(user["_id"]), expires_delta=datetime.timedelta(days=1))
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 201
    
    if hr:
        if not check_password_hash(hr["password"], password):
            return jsonify({"msg": "Invalid Credentials"}), 401
        
        access_token=create_access_token(identity=str(hr["_id"]), expires_delta=datetime.timedelta(days=1))
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": str(hr["_id"]),
                "username": hr["username"],
                "email": hr["email"],
                "role": hr["role"]
            }
        }), 201
    

    return jsonify({"msg": "Something went wrong"}), 500
