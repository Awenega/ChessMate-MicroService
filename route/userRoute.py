from flask import Blueprint, make_response, jsonify, request
from database.query import get_user_db, insert_user_db
from model.user import UserSchema

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    user_info = get_user_db(id)
    user_schema = UserSchema().dump(user_info)
    return make_response(jsonify(user_schema),200)

@user_bp.route('/user', methods=['POST'])
def insert_user():
    parameters = request.json
    user_info = UserSchema().load(parameters)
    print(user_info)
    msg, code = insert_user_db(user_info)
    return make_response(jsonify(msg), code)