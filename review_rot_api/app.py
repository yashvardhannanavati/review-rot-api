from subprocess import check_output
import json

from flask import Flask, request, jsonify
from werkzeug.contrib.cache import SimpleCache

CACHE_TIMEOUT = 300


app = Flask(__name__)
cache = SimpleCache()


def insert_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Method'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

app.after_request(insert_headers)


class cached(object):

    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response
        return decorator


@app.route('/')
@cached()
def get_pr_data():
    rv = check_output(['review-rot', '-c', 'factory2.yaml', '-f', 'json', '--reverse'])
    return jsonify(json.loads(rv))
