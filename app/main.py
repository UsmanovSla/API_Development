# C:\Users\usman\Desktop\Interview\API_Course\envAPI\Scripts\activate.bat
# uvicorn app.main:app --reload
# pip freeze -> requirements.txt

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings


settings = Settings()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
