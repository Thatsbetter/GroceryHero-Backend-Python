from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from backend.config import Credential

Base = declarative_base()
conn_string = Credential().get_conn_uri()

db = create_engine(conn_string)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String)
    age = Column(Integer)
    rating = Column(Float)

    # One-to-Many relationship with carts created by the user
    created_carts = relationship('Cart', backref='creator', foreign_keys='Cart.user_id')

    # One-to-Many relationship with carts delivered by the user
    delivered_carts = relationship('Cart', backref='deliverer', foreign_keys='Cart.deliverer_id')
