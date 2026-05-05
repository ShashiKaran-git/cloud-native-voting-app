from flask import Flask, render_template, request, make_response, g
import redis
import os
import socket
import random
import json

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'redis'),
            port=6379,
            db=0
        )
    return g.redis

@app.route("/", methods=['GET', 'POST'])
def index():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None
    if request.method == 'POST':
        vote = request.form.get('vote')
        if vote:
            get_redis().rpush('votes', json.dumps({'voter_id': voter_id, 'vote': vote}))

    resp = make_response(render_template('index.html', vote=vote, hostname=socket.gethostname()))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)