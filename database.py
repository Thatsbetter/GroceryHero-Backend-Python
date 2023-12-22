
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Credential
class Database:
    def __init__(self):
        database_url = Credential().get_conn_uri()
        self.engine = create_engine(database_url, pool_size=10, max_overflow=20)
        self.Session = sessionmaker(bind=self.engine)

    def create_all_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.Session()
