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
    role=data.get("role")

    if not all ([username, email, password, confirm_password, role]):
        return jsonify({"msg": "All fields are required"}), 400
    
    if password!=confirm_password:
        return jsonify({"msg": "Passwords do not match"}), 400
    
    if mongo.db.users.find_one({"email":email}):
        return jsonify({"msg": "User already exists"}), 400
    
    hashed=generate_password_hash(password)
    mongo.db.users.insert_one({
        "username":username,
        "email":email,
        "password":hashed,
        "role":role
    })

    return jsonify({"msg": "success"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    if not all ([email, password]):
        return jsonify({"msg": "Email and password are required"}), 400
    
    users=mongo.db.users
    user=users.find_one({"email":email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    access_token=create_access_token(identity={"email":user["email"], "role":user["role"]}, expires_delta=datetime.timedelta(hours=24))
    return jsonify({"token": access_token, "role": user["role"]}), 200
