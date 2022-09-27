from helpers.awsResource  import data as dynamodb
from helpers.error import error_500, error_401, error_404
from flask import make_response, jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
dataRoute = Blueprint("data", __name__)

@dataRoute.route("/data", methods=["GET"])
@jwt_required()
def data():
  if request.method == "GET":
    try:
      table = dynamodb.Table('covid')
      print("Data")
      response = table.scan()
      return make_response(jsonify({"Data": response}))
    except Exception as ex:
      return error_500(ex)