from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg
# from psycopg.rows import dict_row


# SQLALCHEMY_DATABASE_URL = 'postsresql://<username>:<password>@<ip-address/hostname>/<databanse_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=12345 port=5432",
#                             row_factory=dict_row)
#     cursor = conn.cursor()
# except Exception as error:
#     print('Connection to databse failed!')
#     print(f'Error: {error}')
# else:
#     print('Database connection was succesfull!')
