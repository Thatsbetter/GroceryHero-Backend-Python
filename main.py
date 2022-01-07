import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, and_
from sqlalchemy.orm.session import sessionmaker
import os
from models.user import User, Base

# Get salt from file, if existent, else generate new salt
SALT = getSalt()

conn_string = "sqlite:///data/smartshopping.db"
engine = create_engine(conn_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
api = Api(app)


class RegisterUser(Resource):
    def post(self):
        status = 400
        request_data = request.get_json()

        # TODO Check if "name","password",... exists in request_data

        if request_data is not None:
            name = request_data.get("name")
            password = request_data.get("password")
            age = request_data.get("age")
            email = request_data.get("email")
            location = request_data.get("location")

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


class CheckLoginDetails(Resource):
    def post(self):
        status = 402
        request_data = request.get_json()
        if request_data is not None:

            email = request_data.get("email")
            password = request_data.get("password")

            result = session.query(User).filter(User.email == email).all()
            session.close()

            if (len(result) == 1):
                user = result[0]
                id = user.id
                hash = user.password

                if (checkPasswordHash(password, hash)):
                    status = 200
                else:
                    status = 401

        return jsonify({
            "status": status
        })


class DeleteUser(Resource):
    def post(self):
        status = 400
        request_data = request.get_json()
        if request_data is not None:
            name = request_data.get("name")
            email = request_data.get("email")
            if checkUserExists(email):
                # checks if name and email are the same
                address = session.query(User).filter(
                    and_(User.email == email,
                         User.name == name))
                address.delete()
                session.commit()
                session.close()

                status = 200

        return jsonify({
            "status": status
        })


def checkUserExists(email):
    users = session.query(User).filter(User.email == email).all()
    session.close()

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


def getSalt():
    salt = bcrypt.gensalt()

    # Check if there is a file called salt.txt
    if (os.path.exists("salt.txt")):
        with open("salt.txt") as file:
            salt = file.readline()
    else:
        # Create new file for the generated salt
        with open("salt.txt", "w") as file:
            file.write(salt)

    return salt


api.add_resource(RegisterUser, "/api/registerUser")
api.add_resource(CheckLoginDetails, "/api/checkLoginDetails")
api.add_resource(DeleteUser, "/api/deleteUser")

if (__name__ == "__main__"):
    app.run(host="0.0.0.0",port=1111)
