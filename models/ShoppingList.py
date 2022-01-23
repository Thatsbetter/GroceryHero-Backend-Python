from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

from databasecredential import Credential

Base = declarative_base()
conn_string = Credential.get_conn_uri()
db = create_engine(conn_string)


class ShoppingList(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True)
    item1 = Column(Integer)  # , ForeignKey(ShoppingItem.id))
    item2 = Column(Integer)  # , ForeignKey(ShoppingItem.id))
    item3 = Column(Integer)  # , ForeignKey(ShoppingItem.id))
    status = Column(String)
    created_by = Column(Integer)  # , ForeignKey(RegisteredUser.id))
    allow_multiple_shoppers = Column(BOOLEAN)


Base.metadata.create_all(db)
