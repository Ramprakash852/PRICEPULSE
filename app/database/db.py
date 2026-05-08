from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def build_default_database_url() -> str:
    db_path = Path(__file__).resolve().parent / "pricepulse.sqlite3"
    return f"sqlite:///{db_path.as_posix()}"


def normalize_database_url(raw_url: str) -> str:
    url = raw_url.strip().strip('"').strip("'")

    if url.lower().startswith("database_url="):
        url = url.split("=", 1)[1].strip()

    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    return url


DATABASE_URL = normalize_database_url(DATABASE_URL or "")

try:
    make_url(DATABASE_URL)
except ArgumentError as exc:
    DATABASE_URL = build_default_database_url()

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Database connected successfully!")
except Exception as e:
    print("Error:", e)