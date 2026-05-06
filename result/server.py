from flask import Flask, render_template
import psycopg2
import os
import time

app = Flask(__name__)

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'votes')

def get_votes():
    while True:
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                dbname=POSTGRES_DB,
                connect_timeout=5
            )
            cursor = conn.cursor()
            cursor.execute("SELECT vote, COUNT(id) FROM votes GROUP BY vote")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            votes = {'Cats': 0, 'Dogs': 0}
            total = 0
            for row in rows:
                votes[row[0]] = row[1]
                total += row[1]

            return votes, total

        except Exception as e:
            print(f"DB error: {e}")
            time.sleep(2)

@app.route("/")
def index():
    votes, total = get_votes()

    cats = votes.get('Cats', 0)
    dogs = votes.get('Dogs', 0)

    cats_percent = round((cats / total * 100), 1) if total > 0 else 0
    dogs_percent = round((dogs / total * 100), 1) if total > 0 else 0

    return render_template('result.html',
        cats=cats,
        dogs=dogs,
        total=total,
        cats_percent=cats_percent,
        dogs_percent=dogs_percent
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)