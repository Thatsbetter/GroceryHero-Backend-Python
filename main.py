import os

import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from databasecredential import Credential
from models.RegisteredUser import RegisteredUser
from models.ShoppingItem import ShoppingItem
from models.ShoppingList import ShoppingList

conn_string = Credential().get_conn_uri()

db = create_engine(conn_string)
base = declarative_base()
base.metadata.create_all(db)

Session = sessionmaker(db)
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
User Management Endpoints
'''

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

                new_user = RegisteredUser(name=name, age=age, email=email, password=hash, location=location)
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

            result = session.query(RegisteredUser).filter(RegisteredUser.email == email).all()
            session.close()

            if (len(result) == 1):
                user = result[0]
                hash = user.password

                if (checkPasswordHash(password, hash)):
                    status = 200
                else:
                    status = 401
            else:
                status = 404
        else:
            status = 418

        return jsonify({
            "status": status
        })


'''
API Endpoint to delete a existing User
TODO secure endpoint so not everyone can just delete a user 

@:param: email (string)      : email to login
@:param: password (string)   : password to login

@:return 200 : if user has been successfully deleted
@:return 400 : Error while trying to delete the user
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

'''
A Endpoint to create a new Shopping List
TODO add status codes as response

@:param: item1 (json)   : First item of the shopping list (send as json)
@:param: item2 (json)   : Second item of the shopping list (send as json)
@:param: item3 (json)   : Third item of the shopping list (send as json) 
@:param: status (string)    : Current status of the shopping list (e.g open, closed)
@:param: created_by (integer)  : creator of the shopping list
@:param: allow_multiple_shoppers (boolean)  : Allow multiple shoppers to participate in finishing the list

@:return 201 : TODO
'''


class CreateShoppingList(Resource):
    def post(self):
        status = 400
        required_params = {"item1", "item2", "item3", "status", "created_by", "allow_multiple_shoppers"}
        request_data = request.get_json()

        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            {"status", "created_by", "allow_multiple_shoppers"})):
            item1 = request_data.get("item1")
            item2 = request_data.get("item2")
            item3 = request_data.get("item3")
            status = request_data.get("status")
            created_by = request_data.get("created_by")
            allow_multiple_shoppers = request_data.get("allow_multiple_shoppers")

            # Create single shopping items if existent
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
            status = 201
            return jsonify({
                "status": status
            })


'''
A Class to change Shopping List´s Status
Data is given using post Method
it checks if all the parameters exist and request is not empty
then changes the status of Shopping List

@:param: id (integer)     : id of the Shopping List
@:param: status (string)  : new status of the Shopping List (open, closed)

@:return 200 : if Status Changed Successfully 
@:return 404 : if Shopping List does not exist
@:return 400 : if data is not in a correct form or has missing parameters
'''
class ChangeShoppingListStatus(Resource):
    def post(self):
        request_data = request.get_json()
        required_params = {"id", "status"}
        status = 400
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
            shoppinglist_id = request_data.get("id")
            new_status = request_data.get("status")
            if (shopping_list_exists(shoppinglist_id)):
                shoppinglist = session.query(ShoppingList).filter((ShoppingList.id == shoppinglist_id))
                shoppinglist.status = new_status
                status = 200
                session.commit()
                session.close()

            else:
                status = 404

        return jsonify({
            "status": status
        })


'''
A Class to change Shopping Item´s Status

@:param: id (integer)     : id of the Shopping List
@:param: status (string)  : new status of the Shopping Item (open, shopping, closed)

@:return 200 : if Status Changed Successfully 
@:return 404 : if Shopping Item does not exist
@:return 400 : if data is not in a correct form or has missing parameters
'''
class ChangeShoppingItemStatus(Resource):
    def post(self):
        request_data = requests.get_json()
        required_params = {"id", "status"}
        status = 400
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(), required_params)):
            shoppingitem_id = request_data.get("id")
            new_status = request_data.get("status")
            if (shopping_item_exists(shoppingitem_id)):
                shoppingitem = session.query(ShoppingItem).filter(ShoppingItem.id == shoppingitem_id)
                shoppingitem.status = new_status
                status = 200
                session.commit()
                session.close()
            else:
                status = 404

        return jsonify({
            "status": status
        })


'''
Helper Methods
'''

'''
A Function to check if a user already in database exists

@:param: email (string) : email that user is registered with it

@:return: True : if user exists
@:return: False : if user does not exist
'''


def checkUserExists(email):
    users = session.query(RegisteredUser).filter(RegisteredUser.email == email).all()
    session.close()

    exists = False

    if (len(users) > 0):
        exists = True

    return exists


'''
A Function that checks, if there is a shoppinglist for the given id

@:param: shoppinglist_id (integer) : the id of the shoppinglist to check

@:return: True : shoppinglist exists
@:return: False : shoppinglist doesnt exist
'''
def shopping_list_exists(shoppinglist_id):
    shopping_lists = session.query(ShoppingList).filter(ShoppingList.id == shoppinglist_id).all()
    session.close()

    return (len(shopping_lists) > 0)


'''
A Function that checks, if there is a shoppingitem for the given id

@:param: shoppingitem_id (integer) : the id of the shoppingitem to check

@:return: True : shoppingitem exists
@:return: False : shoppingitem doesnt exist
'''
def shopping_item_exists(shoppingitem_id):
    shopping_items = session.query(ShoppingItem).filter(ShoppingItem.id == shoppingitem_id).all()
    session.close()

    return (len(shopping_items) > 0)


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


# assigning routs to each class

# /user
api.add_resource(RegisterUser, "/api/user/register")
api.add_resource(CheckLoginDetails, "/api/user/login")
api.add_resource(DeleteUser, "/api/user/delete")

# /shoppinglist
api.add_resource(CreateShoppingList, "/api/shoppinglist/create")
api.add_resource(ChangeShoppingListStatus, "/api/shoppinglist/status")

# /shoppingitem
api.add_resource(ChangeShoppingItemStatus, "/api/shoppingitem/status")


if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=1111)
