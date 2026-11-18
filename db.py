import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def getDB():
    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )
    return conn