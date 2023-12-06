from flask_restful import Resource, Api
import json
from flask import Flask, jsonify, request, make_response
from database.query import delete_user_db, get_user_db, insert_user_db, update_user_db
from model.user import UserSchema

app = Flask(__name__)
api = Api(app)


def validate_token(request):
    token = request.headers.get('token')
    return token == credentials.get('token')


def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
            return credentials
    except FileNotFoundError:
        print("File containing credentials not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON in credentials")
        return None


credentials = load_credentials()
database = f"dbname={credentials.get('dbname')} user={credentials.get('user')} host='{credentials.get('host')}' password='{credentials.get('password')}'"


class UserResource(Resource):
    def get(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 400)

        user_info = get_user_db(id, database)
        if user_info is None:
            return make_response(jsonify({'msg': f'No User found for id: {id}'}), 400)
        else:
            user_schema = UserSchema().dump(user_info)
            return make_response(jsonify(user_schema), 200)

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


api.add_resource(UserResource, '/api/v1/user', '/api/v1/user/<string:id>')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
