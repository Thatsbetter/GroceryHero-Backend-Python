from sqlalchemy.orm import sessionmaker

from config import Credential

DATABASE_URL = Credential().get_conn_uri()

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)
