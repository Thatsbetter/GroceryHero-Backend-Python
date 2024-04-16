from databasecredential import Credential
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn_string = Credential().get_conn_uri()
db = create_engine(conn_string)


class ShoppingItem(Base):
        __tablename__ = "shopping_item"
        id = Column(Integer, primary_key=True)
        product = Column(String, ForeignKey('product.product_id'), nullable=False)
        quantity = Column(Integer, nullable=False)

Base.metadata.create_all(db)
