from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from databasecredential import Credential

Base = declarative_base()
conn_string = Credential.get_conn_uri()

db = create_engine(conn_string)


class RegisteredUser(Base):
    __tablename__ = "registered_user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String, nullable=False)


Base.metadata.create_all(db)
