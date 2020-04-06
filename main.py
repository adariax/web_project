from load_palletes_from_lospec import load_palettes

from flask import make_response, jsonify, render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
