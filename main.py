from flask import Flask, render_template
import requests
from data.kgs import KGS
import json

app = Flask(__name__)
api = KGS("login", "password", "ru_RU")


@app.route('/')
@app.route('/index')
def index():
    return render_template('table.html', title="Главная", users=api.parse_top_100())


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
