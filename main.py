import random
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str | int
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2},
            ]


@app.get("/")
def root():
    return {"message": "Hello world!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = random.randint(0, 10_000_000)
    my_posts.append(post_dict)
    return {"data": post}


@app.get('/posts/{id}')
def get_post(id):
    print(id)
    return {"post_detaile": f"Post with id: {id}"}
