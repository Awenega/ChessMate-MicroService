from flask_restful import Resource
import json
from flask import jsonify, request, make_response, send_from_directory
from database.queriesUser import delete_user_db, get_user_db, insert_user_db, update_user_db
from model.user import UserSchema
import os
import shutil

def validate_token(request):
    token = request.headers.get('Authorization')
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


postgres_credentials = load_credentials()
database = f"dbname={postgres_credentials.get('dbname')} user={postgres_credentials.get('user')} host={postgres_credentials.get('host')} password={postgres_credentials.get('password')}"


class UserResource(Resource):
    def get(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)
        user_info = get_user_db(id, database)

        if user_info is None:
            return make_response(jsonify({'msg': f'No User found for id: {id}'}), 204)
        else:
            user_schema = UserSchema().dump(user_info)
            return make_response(jsonify(user_schema), 200)

    def post(self):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)

        parameters = request.json
        user_info = UserSchema().loads(parameters)
        msg, code = insert_user_db(user_info, database)
        return make_response(jsonify(msg), code)

    def put(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)

        if 'application/json' in request.content_type:
            parameters = json.dumps(request.json)
        else:
            parameters = request.form.get('json_data')
            profilePictureUrl = json.loads(parameters)['profilePictureUrl']
            path = f"assets/user_images/{id}"
            if not os.path.exists(path): 
                os.makedirs(path) 
            if os.listdir(path):
                files = os.listdir(path)
                for file in files:
                    file_path = os.path.join(path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            request.files['file'].save(f"{path}/{profilePictureUrl}")
            print(parameters)

        user_info = UserSchema().loads(parameters)
        msg, code = update_user_db(id, user_info, database)
        return make_response(jsonify(msg), code)

    def delete(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)

        msg, code = delete_user_db(id, database)
        path = f"assets/user_images/{id}"
        if os.path.exists(path): 
            shutil.rmtree(path)
        return make_response(jsonify(msg), code)

class UserImageResource(Resource):
    def get(self, id, profilePictureUrl):
        if profilePictureUrl == "default.jpg":
            return send_from_directory(f"assets/user_images", profilePictureUrl)
        return send_from_directory(f"assets/user_images/{id}", profilePictureUrl)

class UserScore(Resource):
    def put(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)

        reset_score_info = {"id": id, "matchesPlayed": 0, "matchesWon": 0, 'eloRank': 0.0}
        msg, code = update_user_db(id, reset_score_info, database)
        return make_response(jsonify(msg), code)