from datetime import timedelta
from http.client import responses
from helpers.error import error_500, error_401, error_dup_email
from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from flask_bcrypt import generate_password_hash, check_password_hash
import uuid
from boto3.dynamodb.conditions import Attr
from helpers.awsResource  import data as dynamodb
userRoutes = Blueprint("user", __name__)


usersTable = dynamodb.Table("users")


# This route is to create a user
@userRoutes.route("/user/add", methods=["POST"])
def user():
  if request.method == "POST":
    try:
      body = request.get_json()

      # Get the data from the body

      email = body['email']
      firstName = body['firstName']
      lastName = body['lastName']
      password = body['password']

      # Check if the email is in the database already
      response = usersTable.scan(
          FilterExpression=Attr('email').eq(email)
      )
      items = response['Items']

      if len(items) > 0:
        return error_dup_email()

      userId = uuid.uuid1()


      # Create a hashed password has here
      hashedPassword = generate_password_hash(password).decode("utf-8")


      # Create a new user

      usersTable.put_item(
        Item={
          "email": email,
          "firstName": firstName,
          "lastName": lastName,
          "password": hashedPassword,
          "id": str(userId)
        }
      )

      token = create_access_token(identity=userId, expires_delta=timedelta(hours=4))


      return make_response(jsonify({"userId": str(userId), "token": token}))

    except Exception as ex:
      return error_500(ex)

# Logs a user in
@userRoutes.route("/user/login", methods=["POST"])
def login():
  if request.method == "POST":
    try:
      body = request.get_json()

      email = body['email']
      password = body['password']

      # check the email is a user and get that user
      response = usersTable.scan(
          FilterExpression=Attr('email').eq(email)
      )
      items = response['Items']
      if len(items) <= 0:
        return make_response(jsonify({"message": "Email address not found"}), 404)

      user = items[0]


      # Check the password is correct
      isMatch = check_password_hash(user['password'], password)

      if not isMatch:
        return make_response(jsonify({"message": "Incorrect Password"}), 404)

      # Generate JWT
      token = create_access_token(identity=user['id'], expires_delta=timedelta(hours=4))

      # Return JWT
      return make_response(jsonify({"token": token}))
    except Exception as ex:
      return error_500(ex)
