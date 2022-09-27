from flask import jsonify, make_response


def error_500(ex):
    return make_response(jsonify({"message": str(ex)}), 500)


def error_401(ex):
    return make_response(jsonify({"message": ex if ex != "" else "You do not have permission to do that"}), 401)

def error_dup_email():
    return make_response(jsonify({"message": "That email address already exist"}), 403)


def error_404(ex):
    return make_response(jsonify({"message": ex if ex != "" else "We have no record of that item or page"}), 404)


def error_422():
    return make_response(jsonify({'message': "You are missing paramaters needed for this request"}))
