# C:\Users\usman\Desktop\Interview\API_Course\envAPI\Scripts\activate.bat
# uvicorn app.main:app --reload
# pip freeze -> requirements.txt

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=12345 port=5432", row_factory=dict_row)
    cursor = conn.cursor()
except Exception as error:
    print('Connection to databse failed!')
    print(f'Error: {error}')
else:
    print('Database connection was succesfull!')


@app.get("/")
def root():
    return {"message": "Hello world!!!"}


@app.get("/posts")
def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * ''',
                   (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute('''SELECT * FROM posts WHERE id = %s RETURNING *''', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''',
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not exist")

    return {"data": updated_post}
