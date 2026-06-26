from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
import os

from database import get_connection

router = APIRouter()

TOKEN_EXPIRY_HOURS = 8

def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(body: RegisterRequest):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT user_id
            FROM users
            WHERE username = %s
            """,
            (body.username,)
        )

        if cur.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

        cur.execute(
            """
            INSERT INTO users
            (username, password_hash)
            VALUES (%s, %s)
            """,
            (
                body.username,
                password_hash
            )
        )

        conn.commit()

        return {
            "success": True,
            "message": "User created successfully"
        }

    finally:
        cur.close()
        conn.close()


@router.post("/login")
def login(body: LoginRequest):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT password_hash
            FROM users
            WHERE username = %s
            """,
            (body.username,)
        )

        user = cur.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        password_hash = user[0]

        if not bcrypt.checkpw(body.password.encode(), password_hash.encode()):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        token = create_access_token(body.username)

        return {
            "success": True,
            "access_token": token,
            "username": body.username
        }

    finally:
        cur.close()
        conn.close()