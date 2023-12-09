from flask_restful import Api
import json
from flask import Flask
from firebase_admin import credentials, initialize_app, firestore
from serviceUser import UserResource
from serviceOnline import OnlineResource


app = Flask(__name__)
api = Api(app)

# Initialize Firestore DB
cred = credentials.Certificate("firestore.json")
default_app = initialize_app(cred)
db = firestore.client()

api.add_resource(UserResource, '/api/v1/user', '/api/v1/user/<string:id>')
api.add_resource(OnlineResource, '/api/v1/online', '/api/v1/online/<string:id>',
                 resource_class_kwargs={'db': db})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
