from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RegisteredUser(Base):
        __tablename__ = "registered_user"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        age = Column(Integer)
        email = Column(String)
        password = Column(String)
        location = Column(String)
