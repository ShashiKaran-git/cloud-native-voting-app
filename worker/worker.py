import redis
import psycopg2
import json
import os
import time

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'votes')

def get_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                dbname=POSTGRES_DB
            )
            print("Connected to PostgreSQL!")
            return conn
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)

def get_redis():
    while True:
        try:
            r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
            r.ping()
            print("Connected to Redis!")
            return r
        except redis.exceptions.ConnectionError:
            print("Waiting for Redis...")
            time.sleep(2)

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id VARCHAR(255) NOT NULL UNIQUE,
            vote VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    print("Database initialized!")

def process_votes(r, conn):
    cursor = conn.cursor()
    while True:
        try:
            _, data = r.blpop('votes')
            vote_data = json.loads(data)
            voter_id = vote_data['voter_id']
            vote = vote_data['vote']

            cursor.execute("""
                INSERT INTO votes (id, vote) VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE SET vote = EXCLUDED.vote
            """, (voter_id, vote))
            conn.commit()
            print(f"Processed vote: {voter_id} voted for {vote}")

        except Exception as e:
            print(f"Error processing vote: {e}")
            conn.rollback()
            time.sleep(1)

if __name__ == "__main__":
    print("Worker starting...")
    r = get_redis()
    conn = get_postgres()
    init_db(conn)
    print("Worker ready — listening for votes...")
    process_votes(r, conn)