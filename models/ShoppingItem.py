from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = create_engine("postgresql://smartshopping:smartshopping@127.0.0.1:5432/smartshopping")


class ShoppingItem(Base):
        __tablename__ = "shopping_item"
        id = Column(Integer, primary_key=True)
        product = Column(String)
        count = Column(Integer)
        shopper = Column(Integer) #, ForeignKey(RegisteredUser.id))
        status = Column(String)

        # registered_user = relationship('RegisteredUser', foreign_keys='ShoppingItem.id')

Base.metadata.create_all(db)