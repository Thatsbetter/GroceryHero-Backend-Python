from sqlalchemy import create_engine, delete
from sqlalchemy.orm.session import sessionmaker
from models.user import User, Base
from flask import Flask, jsonify, request
import bcrypt
import json


SALT = bcrypt.gensalt()

conn_string = "sqlite:///data/smartshopping.db"
engine = create_engine(conn_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route("/api/registerUser", methods=["POST"])
def registerUser():
    request_data = request.get_json()
    name = request_data.get("name")
    password = request_data.get("password")
    age = request_data.get("age")
    email = request_data.get("email")
    location = request_data.get("location")

    status = 400

    if (not checkUserExists(email)):
        # Generate new Password Hash
        hash = generatePasswordHash(password).hex()

        new_user = User(name=name, age=age, email=email, password=hash, location=location)
        session.add(new_user)
        session.commit()

        status = 201
    else:
        # User already exists
        status = 409

    return jsonify({
        "status": status,
    })

@app.route("/api/checkLoginDetails", methods=["POST"])
def checkLoginDetails():
    request_data = request.get_json()
    email = request_data.get("email")
    password = request_data.get("password")

    status = 402

    result = session.query(User).filter(User.email == email).all()

    if (len(result) == 1):
        user = result[0]
        id = user.id
        hash = user.password

        if (checkPasswordHash(password, hash)):
            status = 200
        else:
            status = 401

    return jsonify({
        "status" : status
    })

@app.route("/api/deleteUser", methods=["POST"])
def deleteUser():
    request_data = request.get_json()
    name = request_data.get("name")

    # TODO
    users = session.query(User).filter(User.name == name).all()

    delete = User.delete().where(User.name == name)
    delete.execute()

    return {"test": "test"}

def checkUserExists(email):
    users = session.query(User).filter(User.email == email).all()

    exists = False

    if (len(users) > 0):
        exists = True

    return exists

def generatePasswordHash(password):
    password = password.encode()

    hash = bcrypt.hashpw(password, SALT)
    return hash

def checkPasswordHash(password, storedHash):
    password = password.encode()
    generatedHash = bcrypt.hashpw(password, SALT)

    match = False

    if (generatedHash.hex() == storedHash):
        match = True

    return match

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=1111)
