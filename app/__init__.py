from flask import Flask
from blueprints.test import testRoute
from blueprints.data import dataRoute 
from blueprints.user import userRoutes
from flask_jwt_extended import JWTManager
from helpers.getSecret import get_secret
from flask_cors import CORS

def create_app():
  jwt_secret = get_secret("jwt-secret-key", "us-west-1")
  app = Flask(__name__)
  app.register_blueprint(testRoute)
  app.register_blueprint(dataRoute)
  app.register_blueprint(userRoutes)
  app.config[
        "JWT_SECRET_KEY"] = jwt_secret['JWT_SECRET_KEY']
  JWTManager(app)
  CORS(app)
  return app