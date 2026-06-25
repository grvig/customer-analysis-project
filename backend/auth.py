from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

from database import get_connection

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


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

        password_hash = pwd_context.hash(body.password)

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

        if not pwd_context.verify(
            body.password,
            password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        return {
            "success": True,
            "message": "Login successful",
            "username": body.username
        }

    finally:
        cur.close()
        conn.close()