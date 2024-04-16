from databasecredential import Credential
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn_string = Credential().get_conn_uri()
db = create_engine(conn_string)


class ShoppingItem(Base):
        __tablename__ = "address"
        id = Column(Integer, primary_key=True)
        country = Column(String, nullable=False)
        city = Column(String, nullable=False)
        street = Column(String, nullable=False)
        house_number = Column(Integer, nullable=True)
        postal_code = Column(Integer, nullable=False)
        additional_comment = Column(String, nullable=True)
