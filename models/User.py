from databasecredential import Credential
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn_string = Credential().get_conn_uri()

db = create_engine(conn_string)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

