from flask import make_response, jsonify

from app import app


@app.route('/')
@app.route('/index')
def index():
    return make_response(jsonify({'page': 'page'}))


if __name__ == '__main__':
    app.run()
