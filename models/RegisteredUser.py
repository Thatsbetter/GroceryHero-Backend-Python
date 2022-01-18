from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
db = create_engine("postgresql://smartshopping:smartshopping@127.0.0.1:5432/smartshopping")


class RegisteredUser(Base):
        __tablename__ = "registered_user"
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        age = Column(Integer, nullable=False)
        email = Column(String, nullable=False)
        password = Column(String, nullable=False)
        location = Column(String, nullable=False)

Base.metadata.create_all(db)
