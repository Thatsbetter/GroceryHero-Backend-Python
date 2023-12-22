import logging
import os

import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from payment.payment_controller import *
from cart.cart_controller import *
from user.user_controller import *
from sqlalchemy.orm.session import sessionmaker
import stripe




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


def checkPasswordHash(password, storedHash):
    password = password.encode()
    generatedHash = bcrypt.hashpw(password, SALT)

    return (generatedHash.hex() == storedHash)





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
    app.run(debug=True,host="0.0.0.0", port=1111)
