import psycopg2
from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Conexão conclúida: ", conn)
    except Exception as e:
        print("Ocorreu um erro:", e)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)