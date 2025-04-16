import pytest
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASS = os.getenv("DB_PASSWORD")


@pytest.fixture
def db_config():
    return {
        'type': 'postgresql',
        'dbname': 'postgres',
        'user': "akhil",
        'password': DB_PASS,
        'port':"5432",
    }
