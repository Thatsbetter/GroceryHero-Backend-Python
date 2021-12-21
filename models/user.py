from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
        __tablename__ = "user"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        age = Column(Integer)
        email = Column(String)
        password = Column(String)
        location = Column(String)
