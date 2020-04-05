from load_palletes_from_lospec import loading

from flask import make_response, jsonify

from app import app


@app.route('/')
@app.route('/index')
def index():
    return make_response(jsonify({'page': 'page'}))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
