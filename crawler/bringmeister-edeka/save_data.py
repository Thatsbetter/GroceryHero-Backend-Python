import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

from backend.databasecredential import Credential

df = pd.read_csv("simplified_data.csv", index_col="product_id")

connection_string = Credential().get_conn_uri()
engine = create_engine(connection_string)
table_name = 'edeka_products'

df.to_sql(table_name, engine, if_exists='replace', index=True)

with engine.connect() as con:
    con.execute(text(f'ALTER TABLE {table_name} ADD PRIMARY KEY (product_id);'))
    con.commit()
