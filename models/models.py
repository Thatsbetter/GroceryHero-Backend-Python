from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.databasecredential import Credential

Base = declarative_base()
conn_string = Credential().get_conn_uri()
db = create_engine(conn_string)
metadata = MetaData()


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house_number = Column(Integer, nullable=True)
    postal_code = Column(Integer, nullable=False)
    additional_comment = Column(String, nullable=True)


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    supermarket = Column(String, nullable=True)
    name = Column(String, nullable=False)
    categories = Column(String, nullable=True)
    price = Column(String, nullable=True)
    packing = Column(String, nullable=True)
    image = Column(String, nullable=False)


class ShoppingList(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey('public.user.id'))
    delivery_address = Column(Integer, ForeignKey('public.address.id'))


class ShoppingItem(Base):
    __tablename__ = "shopping_item"
    id = Column(Integer, primary_key=True)
    shopping_list = Column(Integer, ForeignKey('shopping_list.id'), nullable=False)
    product = Column(String, ForeignKey('product.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    @classmethod
    def user_exists(cls, email):
        with Session(db) as session:
            with session.begin():
                user = session.query(cls).filter_by(email=email).first()
                return user is not None

    @classmethod
    def authenticate(cls, email, password):
        with Session(db) as session:
            with session.begin():
                user = session.query(cls).filter_by(email=email, password=password).first()
                return user is not None

    @classmethod
    def delete_user(cls, email):
        with Session(db) as session:
            with session.begin():
                user = session.query(cls).filter_by(email=email).first()
                if user:
                    session.delete(user)
                    return True
                else:
                    return False


metadata.create_all(db)
