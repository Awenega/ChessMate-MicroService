from flask_restful import Resource
import json
from flask import jsonify, request, make_response
from database.queriesMatches import get_matches_db, insert_match_db
from model.match import MatchSchema


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


class MatchResource(Resource):
    def get(self, id):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)
        matchesList = get_matches_db(id, database)
        
        if matchesList is None:
            return make_response(jsonify({'msg': f'No matches found for userid: {id}'}), 204)
        else:
            match_schema = MatchSchema(many=True).dump(matchesList)
            return make_response(jsonify(match_schema), 200)
    
    def post(self):
        if not validate_token(request):
            return make_response(jsonify({'msg': 'Unauthorized. Invalid or missing token.'}), 401)

        parameters = request.json
        match_info = MatchSchema().loads(parameters)
        msg, code = insert_match_db(match_info, database)
        return make_response(jsonify(msg), code)

