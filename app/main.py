# C:\Users\usman\Desktop\Interview\API_Course\envAPI\Scripts\activate.bat
# uvicorn app.main:app --reload
# pip freeze -> requirements.txt

from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row

from . import models
from .database import engine
from routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=12345 port=5432", row_factory=dict_row)
    cursor = conn.cursor()
except Exception as error:
    print('Connection to databse failed!')
    print(f'Error: {error}')
else:
    print('Database connection was succesfull!')


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello world!!!"}
