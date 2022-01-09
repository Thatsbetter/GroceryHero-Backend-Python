import os

import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, and_
from sqlalchemy.orm.session import sessionmaker

from models.user import User, Base

conn_string = "sqlite:///data/smartshopping.db"
engine = create_engine(conn_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
api = Api(app)

'''
A Function to generate Salt for hashing
it checks if a file exists, which has Salt within
if not it will generate a salt and saves it in a file

'''


def getSalt():
    salt = bcrypt.gensalt().hex()

    # Check if there is a file called salt.txt
    if (os.path.exists("salt.txt")):
        with open("salt.txt") as file:
            salt = file.readline()
    else:
        # Create new file for the generated salt
        with open("salt.txt", "w") as file:
            file.write(salt)

    return salt


# Get salt from file, if existent, else generate new salt
SALT = bytes.fromhex(getSalt())

'''
A Class to register a user
Data is given using post Method
it checks if all the parameters exist and request is not empty
then saves it to database

@:param: email (string)     : email to login
@:param: password (string)  : password to login
@:param: name  (string)     : name of the user 
@:param: age (string)       : age of the user
@:param: location (string)  : user´s location

@:return 201 : if new user created
@:return 409 : if user already exists
@:return 418 : if data is not in a correct form or has missing parameters


'''


class RegisterUser(Resource):
    def post(self):
        status = 400
        required_params = {"name", "password", "email", "age", "location"}
        request_data = request.get_json()

        # Validate Parameters
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
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
                status = 409
        else:
            status = 418

        return jsonify({
            "status": status,
        })


'''
A Class to check login credential
Data is given using post Method
it checks if all parameters exist and request is not empty
then saves it to database

@:param: email (string)      : email to login
@:param: password (string)   : password to login

@:return 200 : if password is correct
@:return 409 : if password is incorrect
@:return 418 : if data is not in a correct form or has missing parameters


'''


class CheckLoginDetails(Resource):
    def post(self):
        status = 402
        required_params = {"email", "password"}
        request_data = request.get_json()

        # Validate Parameters
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
            email = request_data.get("email")
            password = request_data.get("password")

            result = session.query(User).filter(User.email == email).all()
            session.close()

            if (len(result) == 1):
                user = result[0]
                hash = user.password

                if (checkPasswordHash(password, hash)):
                    status = 200
                else:
                    status = 401
        else:
            status = 418

        return jsonify({
            "status": status
        })


'''
A Class to delete a user
Data is given using post Method
it checks if all the parameters exist and request is not empty
then saves it to database

@:param: email (string)     : email to login
@:param: name  (string)     : name of the user 


@:return 201 : if user is deleted
@:return 400 : email or user does not exist
@:return 418 : if data is not in a correct form or has missing parameters




'''


class DeleteUser(Resource):
    def post(self):
        status = 400
        required_params = {"name", "email"}
        request_data = request.get_json()

        # Validate Parameters
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
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
        else:
            status = 418

        return jsonify({
            "status": status
        })


'''
A Function to check if a user already in database exists

@:param: email (string) : email that user is registered with it

@:return: True : if user exists
@:return: False : if user does not exist

'''


def checkUserExists(email):
    users = session.query(User).filter(User.email == email).all()
    session.close()

    exists = False

    if (len(users) > 0):
        exists = True

    return exists


'''
A Function to generate a hashed password using Salt

@:param: password (string) : the password that user uses to login

@:return: password (string) : a hashed password
'''


def generatePasswordHash(password):
    password = password.encode()

    hash = bcrypt.hashpw(password, SALT)
    return hash


'''
A Function to check if a password matches with the hashed password

@:param: password (string) : password that user uses to login
@:param: password (string) : hashed password that saved in database

@:return: True : if password matches with hashed password
@:return: False : if password does not matches with hashed password

'''


def checkPasswordHash(password, storedHash):
    password = password.encode()
    generatedHash = bcrypt.hashpw(password, SALT)

    return (generatedHash.hex() == storedHash)

'''

a Function to check if all of required Parameters exist in data

@:param data (dict) : received data
@:param requiredParameters (dict) : ??
@:param receivedParameters (dict) : ??
@:param necessaryParameters (dict) : ??

@:return True : if received data has required parameters
@:return False : if received data hasn´t required parameters

'''
def validateParameters(data, requiredParameters, receivedParameters, necessaryParameters):
    valid = True

    if (receivedParameters >= requiredParameters):
        # Check if all necessary parameters are nonempty
        parametersToCheck = receivedParameters & necessaryParameters
        for parameter in parametersToCheck:
            if not (len(data.get(parameter)) > 0):
                valid = False
    else:
        valid = False

    return valid

# assigning routs to each class
api.add_resource(RegisterUser, "/api/registerUser")
api.add_resource(CheckLoginDetails, "/api/checkLoginDetails")
api.add_resource(DeleteUser, "/api/deleteUser")

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=1111)
