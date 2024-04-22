import os

import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

from databasecredential import Credential
from models.models import ShoppingItem, ShoppingList, User

conn_string = Credential().get_conn_uri()

stripe.api_key = Credential().get_stripe_secret_key_test()
stripe_publishable_key = Credential().get_stripe_publishable_key_test()

db = create_engine(conn_string)
base = declarative_base()

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
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, "salt.txt")
    if (os.path.exists(file_path)):
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
'''


class RegisterUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('birthday', type=str, required=True)
        request_data = parser.parse_args()

        name = request_data.get("name")
        password = request_data.get("password")
        email = request_data.get("email")
        age = request_data.get("birthday")

        if (User.user_exists(email)):
            return jsonify({'message': 'User already exists'}), 409

        # Generate new Password Hash
        hash = generatePasswordHash(password).hex()

        new_user = User(name=name, email=email, password=hash, birthday=birthday)
        session.add(new_user)
        session.commit()

        return '', 201


'''
A Class to check login credential
Data is given using post Method
it checks if all parameters exist and request is not empty
then saves it to database

@:param: email (string)      : email to login
@:param: password (string)   : password to login

@:return 200 : if password is correct
@:return 403 : if password is incorrect
'''


class CheckLoginDetails(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        request_data = parser.parse_args()

        email = request_data.get("email")
        password = request_data.get("password")

        hash = generatePasswordHash(password)

        if (User.authenticate(email, hash)):
            return '', 200
        return jsonify({
            "message": 'Incorrect login Details'
        }), 403


'''
API Endpoint to delete a existing User
TODO secure endpoint so not everyone can just delete a user 

@:param: email (string)      : email to login
@:param: password (string)   : password to login

@:return 200 : if user has been successfully deleted
@:return 400 : Error while trying to delete the user
'''


class DeleteUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        request_data = parser.parse_args()

        email = request_data.get("email")

        if (User.delete_user(email)):
            return '', 200
        return jsonify({
            "message": 'Deleting User failed'
        }), 400


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

        if (request_data is not None):
            items = getShoppingItems(request_data)
            status = request_data.get("status")
            created_by = request_data.get("created_by")
            allow_multiple_shoppers = request_data.get("allow_multiple_shoppers")

            item_ids = {
                "item1": None,
                "item2": None,
                "item3": None
            }

            # Create single shopping items
            for item in items.keys():
                new_shopping_item = ShoppingItem(
                    product=request_data[item]["product"],
                    count=request_data[item]["count"],
                    shopper=request_data[item]["shopper"],
                    status=request_data[item]["status"]
                )
                session.add(new_shopping_item)
                session.commit()
                item_ids[item] = new_shopping_item.id

            # Create shopping list
            new_shopping_list = ShoppingList(
                item1=item_ids["item1"],
                item2=item_ids["item2"],
                item3=item_ids["item3"],
                status=status,
                created_by=created_by,
                allow_multiple_shoppers=allow_multiple_shoppers
            )

            session.add(new_shopping_list)
            session.commit()
            status = 201
        else:
            status = 409

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
        request_data = request.get_json()
        required_params = {"id", "status"}
        status = 400
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
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


class CreateStripePayment(Resource):
    def post(self):
        request_data = request.get_json()
        amount = request_data["amount"]

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='eur',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        response = jsonify(paymentIntent=payment_intent.client_secret,
                           publishableKey=stripe_publishable_key
                           )
        return response


class LogStripePaymentError(Resource):
    def post(self):
        request_data = request.get_json()
        logging.error(request_data)


'''
Helper Methods
'''



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
A Function that filters the given items of a POST request

@:param: data (dic) : The data of the POST request

@:return: dic : given items for the POST request
'''


def getShoppingItems(data):
    items_to_test = ["item1", "item2", "item3"]
    items = {}
    for item in items_to_test:
        if (item in data.keys()):
            items[item] = data[item]
    return items


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

# /stripe
api.add_resource(CreateStripePayment, "/api/stripe/create")
api.add_resource(LogStripePaymentError, "/api/stripe/error")

if (__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0", port=1111)
