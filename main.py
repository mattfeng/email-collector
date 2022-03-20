from audioop import cross
from flask import Flask, jsonify, request, Response
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
from flask_cors import cross_origin
import json
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["MONGODB_SETTINGS"] = {
        "host": os.environ.get("DB_HOST", "fakehost"),
        "username": os.environ.get("DB_USER", "fakeuser"),
        "password": os.environ.get("DB_PASS", "fakepass"),
        "port": 27017
    }

    db = MongoEngine()
    db.init_app(app)

    class Email(db.Document):
        email = db.StringField()
    
    @app.route("/")
    def home():
        return "emails"

    @app.route("/add", methods=["POST"])
    @cross_origin(origins=["http://localhost:8000", "https://aceresearch.github.io"])
    def add():
        addr = request.form.get("email")
        print(addr)

        msg = json.dumps({"message": "bad email", "error": True})
        status = 400

        if addr is not None:
            email = Email(email=addr)
            email.save()

            msg = json.dumps({"message": "success", "error": False})
            status = 200
        
        response = Response(response=msg, status=status)
        return response

    @app.route("/emails")
    def emails():
        passwd = request.args.get("password")

        if passwd != os.environ.get("EMAILS_PASSWORD"):
            return "no access"

        emails = [email.email for email in Email.objects()]
        return jsonify(emails)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", debug=True, port=8080)


