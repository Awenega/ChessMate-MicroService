from flask_restful import Resource
import json
from flask import jsonify, request, make_response
from database.queriesUser import delete_user_db, get_user_db, insert_user_db, update_user_db
from helperCelery import handle_game_state
from model.user import UserSchema


def validate_token(request):
    token = request.headers.get('token')
    return token == postgres_credentials.get('token')


def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            postgres_credentials = json.load(f)
            return postgres_credentials
    except FileNotFoundError:
        print("File containing credentials not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON in credentials")
        return None


# POSTGRES DB
postgres_credentials = load_credentials()
database = f"dbname={postgres_credentials.get('dbname')} user={postgres_credentials.get('user')} host={postgres_credentials.get('host')} password={postgres_credentials.get('password')}"


class OnlineResource(Resource):
    def __init__(self, db):
        self.db = db
        self.rooms_ref = db.collection("Rooms")

    def get(self):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 400)
        handle_game_state('provaprova', self.db)

    def post(self):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 400)

        parameters = request.json
        user_info = UserSchema().loads(parameters)
        msg, code = insert_user_db(user_info, database)
        return make_response(jsonify(msg), code)

    def put(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 400)

        parameters = request.json
        user_info = UserSchema().loads(parameters)
        msg, code = update_user_db(id, user_info, database)
        return make_response(jsonify(msg), code)

    def delete(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 400)

        msg, code = delete_user_db(id, database)
        return make_response(jsonify(msg), code)
