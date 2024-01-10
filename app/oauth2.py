from jose import jwt
from datetime import datetime, timedelta
# SECRET_KEY
# Algorithm
# Expriation time

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "dfg62nowef4651npdfger84bs6sdf4h8tyjk46s1g13s0v7qwf7n56672b15z1c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt
