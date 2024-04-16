from databasecredential import Credential
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn_string = Credential().get_conn_uri()
db = create_engine(conn_string)


class ShoppingList(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'))
    delivery_address = Column(Integer, ForeignKey('address.id'))
