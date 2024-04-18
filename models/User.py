from databasecredential import Credential
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn_string = Credential().get_conn_uri()

db = create_engine(conn_string)


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
