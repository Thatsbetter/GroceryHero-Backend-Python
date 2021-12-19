from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from models.user import User, Base
from flask import Flask, jsonify, request
import json


conn_string = "sqlite:///data/smartshopping.db"
engine = create_engine(conn_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route("/api/registerUser", methods=["POST"])
def registerUser():
    request_data = request.get_json()
    username = request_data.get("name")
    password = request_data.get("password")
    age = request_data.get("age")
    email = request_data.get("email")
    location = request_data.get("location")

    new_user = User(name=username, age=age, email=email, password=password, location=location)
    session.add(new_user)
    session.commit()

    return jsonify({
            "status" : "Benutzer wurde erfolgreich erstellt",
            "username" : username,
            "password" : password
        })


@app.route("/api/checkUserExists", methods=["POST"])
def checkUserExists():
	request_data = request.get_json()
	username = request_data.get("name")
	
	result = session.query(User).filter(User.name == username)

	test123 = ""
	for row in result:
		test123 = row.name
	return jsonify(test123)


if (__name__ == "__main__"):
	app.run(port=8080)

