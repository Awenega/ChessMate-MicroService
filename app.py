from flask import Flask
from route.userRoute import user_bp

app = Flask(__name__)

with app.app_context():
    app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)