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
        session = Session()
        user = session.query(cls).filter_by(email=email).first()
        session.close()
        return user is not None

    @classmethod
    def authenticate(cls, email, password):
        session = Session()
        user = session.query(cls).filter_by(email=email, password=password).first()
        session.close()
        return user is not None

    @classmethod
    def delete_user(cls, email):
        session = Session()
        user = session.query(cls).filter_by(email=email).first()
        if user:
            session.delete(user)
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False
