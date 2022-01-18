from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = create_engine("postgresql://smartshopping:smartshopping@127.0.0.1:5432/smartshopping")

class ShoppingList(Base):
        __tablename__ = "shopping_list"
        id = Column(Integer, primary_key=True)
        item1 = Column(Integer) #, ForeignKey(ShoppingItem.id))
        item2 = Column(Integer) #, ForeignKey(ShoppingItem.id))
        item3 = Column(Integer) #, ForeignKey(ShoppingItem.id))
        status = Column(String)
        created_by = Column(Integer) #, ForeignKey(RegisteredUser.id))
        allow_multiple_shoppers = Column(Boolean)

Base.metadata.create_all(db)