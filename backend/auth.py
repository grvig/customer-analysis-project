from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import bcrypt
import os

from database import get_connection

router = APIRouter()

_bearer = HTTPBearer()

TOKEN_EXPIRY_HOURS = 8


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    try:
        jwt.decode(credentials.credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_username_from_token(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/register")
def register(body: RegisterRequest):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT user_id FROM users WHERE username = %s",
            (body.username,)
        )

        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (body.username, password_hash)
        )
        conn.commit()

        return {"success": True, "message": "User created successfully"}

    finally:
        if cur: cur.close()
        if conn: conn.close()


@router.post("/login")
def login(body: LoginRequest):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (body.username,)
        )
        user = cur.fetchone()

        if not user or not bcrypt.checkpw(body.password.encode(), user[0].encode()):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token(body.username)

        return {
            "success": True,
            "access_token": token,
            "username": body.username
        }

    finally:
        if cur: cur.close()
        if conn: conn.close()


@router.post("/change-password")
def change_password(body: ChangePasswordRequest, username: str = Depends(get_username_from_token)):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not bcrypt.checkpw(body.current_password.encode(), user[0].encode()):
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        new_hash = bcrypt.hashpw(body.new_password.encode(), bcrypt.gensalt()).decode()

        cur.execute(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (new_hash, username)
        )
        conn.commit()

        return {"success": True, "message": "Password changed successfully"}

    finally:
        if cur: cur.close()
        if conn: conn.close()
