import json


class Credential():
    def __init__(self):
        with open('credential.json', 'r') as myfile:
            data = myfile.read()
        self.obj = json.loads(data)

    def get_username(self):
        return self.obj["username"]

    def get_password(self):
        return self.obj["password"]

    def get_database_name(self):
        return self.obj["database_name"]

    @staticmethod
    def get_conn_uri():
        return f'postgresql://{self.get_username()}:{self.get_password()}@127.0.0.1:5432/{self.get_database_name()}'
