from databasecredential import Credential
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn_string = Credential().get_conn_uri()
db = create_engine(conn_string)


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    supermarket = Column(String, nullable=True)
    name = Column(String, nullable=False)
    categories = Column(String, nullable=True)
    price = Column(String, nullable=True)
    packing = Column(String, nullable=True)
    image = Column(String, nullable=False)
