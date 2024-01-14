# C:\Users\usman\Desktop\Interview\API_Course\envAPI\Scripts\activate.bat
# uvicorn app.main:app --reload
# pip freeze -> requirements.txt

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote


app = FastAPI()

origins = [
    # "*",   - all domains
    "http://localhost:8080",
    # "https://www.google.com",   - domain google.com
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
