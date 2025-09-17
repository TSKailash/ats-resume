from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.authRoutes import auth_bp
from flask_pymongo import PyMongo
from extensions import mongo, jwt
from dotenv import load_dotenv
import os



def create_app():
    load_dotenv()

    app=Flask(__name__)
    CORS(app)
    app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY", "SUMMA_KEY")
    app.config["MONGO_URI"]=os.getenv("MONGO_URI", "mongodb://localhost:27017/myDatabase")
    mongo.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)