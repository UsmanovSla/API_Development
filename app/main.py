# C:\Users\usman\Desktop\Interview\API_Course\envAPI\Scripts\activate.bat
# uvicorn app.main:app --reload
# pip freeze -> requirements.txt

import random
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


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2},
            ]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello world!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = random.randint(0, 10_000_000)
    my_posts.append(post_dict)
    return {"data": post}


@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index i nthe array
    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not exist")

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
