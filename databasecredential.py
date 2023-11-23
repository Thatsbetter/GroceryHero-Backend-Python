import json
import os

class Credential():
    def __init__(self):
        dir_name = os.path.dirname(__file__)
        file_path = os.path.join(dir_name,'credential.json')
        with open(file_path, 'r') as myfile:
            data = myfile.read()
        self.obj = json.loads(data)

    def get_username(self):
        return self.obj["username"]

    def get_password(self):
        return self.obj["password"]

    def get_database_name(self):
        return self.obj["database_name"]

    def get_conn_uri(self):
        return "postgresql://%s:%s@127.0.0.1:5432/%s" %(self.get_username(), self.get_password(), self.get_database_name())
    def get_stripe_secret_key_test(self):
        return self.obj["stripe-secret-key_test"]
    def get_stripe_publishable_key_test(self):
        return self.obj["stripe_publishable_key_test"]
    def get_paypal_client_id(self):
        return self.obj["paypal-client-id-dev"]

    def get_paypal_secret(self):
        return self.obj["paypal-secret-dev"]
