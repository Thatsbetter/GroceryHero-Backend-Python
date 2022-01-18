import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, and_
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.RegisteredUser import RegisteredUser, Base
from models.ShoppingItem import ShoppingItem
import os


# TODO Save username and password of database somewhere and then load in the variables (not hardcoded in main.py!)
username = "smartshopping"
password = "smartshopping"

conn_string = "postgresql://smartshopping:smartshopping@127.0.0.1:5432/smartshopping"
db = create_engine(conn_string)
base = declarative_base()
base.metadata.create_all(db)

Session = sessionmaker(db)
session = Session()

app = Flask(__name__)
api = Api(app)

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
User Management Endpoints
'''

class RegisterUser(Resource):
    def post(self):
        status = 400
        required_params = {"name", "password", "email", "age", "location"}
        request_data = request.get_json()

        # Validate Parameters
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(), required_params)):
            name = request_data.get("name")
            password = request_data.get("password")
            age = request_data.get("age")
            email = request_data.get("email")
            location = request_data.get("location")

            if (not checkUserExists(email)):
                # Generate new Password Hash
                hash = generatePasswordHash(password).hex()

                new_user = RegisteredUser(name=name, age=age, email=email, password=hash, location=location)
                session.add(new_user)
                session.commit()

                status = 201
            else:
                # User already exists
                status = 409
        else:
            status = 418

        return jsonify({
            "status": status,
        })


class CheckLoginDetails(Resource):
    def post(self):
        status = 402
        required_params = {"email", "password"}
        request_data = request.get_json()

        # Validate Parameters
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(), required_params)):
            email = request_data.get("email")
            password = request_data.get("password")

            result = session.query(RegisteredUser).filter(RegisteredUser.email == email).all()
            session.close()

            if (len(result) == 1):
                user = result[0]
                id = user.id
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


class DeleteUser(Resource):
    def post(self):
        status = 400
        required_params = {"name", "email"}
        request_data = request.get_json()

        # Validate Parameters
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(), required_params)):
            name = request_data.get("name")
            email = request_data.get("email")
            if checkUserExists(email):
                # checks if name and email are the same
                address = session.query(RegisteredUser).filter(
                    and_(RegisteredUser.email == email,
                         RegisteredUser.name == name))
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
Shopping List Management Endpoints
'''

class CreateShoppingList(Resource):
    def post(self):
        required_params = {"item1", "item2", "item3", "status", "created_by", "allow_multiple_shoppers"}
        request_data = request.get_json()

        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(), {"status", "created_by", "allow_multiple_shoppers"})):
            item1 = request_data.get("item1")
            item2 = request_data.get("item2")
            item3 = request_data.get("item3")
            status = request_data.get("status")
            created_by = request_data.get("created_by")
            allow_multiple_shoppers = request_data.get("allow_multiple_shoppers")

            # Create singe shopping items if existent
            new_shopping_item1 = ShoppingItem(
                product=item1["product"],
                count=item1["count"],
                shopper=item1["shopper"],
                status=item1["status"]
            )
            new_shopping_item2 = ShoppingItem(
                product=item2["product"],
                count=item2["count"],
                shopper=item2["shopper"],
                status=item2["status"]
            )
            new_shopping_item3 = ShoppingItem(
                product=item3["product"],
                count=item3["count"],
                shopper=item3["shopper"],
                status=item3["status"]
            )

            session.add(new_shopping_item1)
            session.add(new_shopping_item2)
            session.add(new_shopping_item3)

            # Create shopping list
            new_shopping_list = ShoppingList(
                item1=new_shopping_item1.id,
                item2=new_shopping_item2.id,
                item3=new_shopping_item3.id,
                status=status,
                created_by=created_by,
                allow_multiple_shoppers=allow_multiple_shoppers
            )

            session.add(new_shopping_list)
            session.commit()

'''
Helper Methods
'''

def checkUserExists(email):
    users = session.query(RegisteredUser).filter(RegisteredUser.email == email).all()
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


def validateParameters(data, requiredParameters, receivedParameters, necessaryParameters):
    valid = True

    # Check if all necessary parameters are existent
    if (receivedParameters >= requiredParameters):
        # Check if necessary parameters are nonempty
        parametersToCheck = receivedParameters & necessaryParameters
        for parameter in parametersToCheck:
            if (isinstance((data.get(parameter)), str)):
                if not (len(data.get(parameter)) > 0):
                    valid = False
    else:
        valid = False

    return valid

api.add_resource(RegisterUser, "/api/registerUser")
api.add_resource(CheckLoginDetails, "/api/checkLoginDetails")
api.add_resource(DeleteUser, "/api/deleteUser")

if (__name__ == "__main__"):
    app.run(host="0.0.0.0",port=1111)
