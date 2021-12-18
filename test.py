from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from models.user import User, Base


conn_string = "sqlite:///data/smartshopping.db"
engine = create_engine(conn_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name="test", age=21, email="Mark.Muster@mark.de", password="test", location="Hamburg, Germany")
session.add(new_user)
session.commit()