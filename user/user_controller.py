from models.RegisteredUser import RegisteredUser
from flask_restful import reqparse
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import and_
from sqlalchemy.orm.session import sessionmaker
from user_service import *

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

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        parser.add_argument('age', type=int, required=True, help='Age cannot be blank')
        parser.add_argument('location', type=str, required=True, help='Location cannot be blank')

        args = parser.parse_args()

        name = args['name']
        password = args['password']
        age = args['age']
        email = args['email']
        location = args['location']

        status = self.register_user(age, email, location, name, password)

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

        # Validate Parameters
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')

        args = parser.parse_args()

        password = args['password']
        email = args['email']

        status = self.login_user(email, password)

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

        # Validate Parameters
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')

        args = parser.parse_args()

        name = args['name']
        email = args['email']

        delete_user(name,email)

        status = 200


        return jsonify({
            "status": status
        })
