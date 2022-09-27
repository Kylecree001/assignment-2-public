from helpers.error import error_500, error_401, error_404
from flask import make_response, jsonify, Blueprint, request
testRoute = Blueprint("test", __name__)

@testRoute.route("/test", methods=["GET"])
def test():
  if request.method == "GET":
    try:
      print("Test")
      return make_response(jsonify({"Test": "test"}))
    except Exception as ex:
      return error_500(ex)