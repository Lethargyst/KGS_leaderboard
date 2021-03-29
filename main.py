from flask import Flask, render_template, request, jsonify
from data.kgs import KGS

app = Flask(__name__)
api = KGS("login", "password", "ru_RU")


@app.route('/')
@app.route('/table')
def index():
    return render_template('table.html', users=api.parse_top_100())


@app.route('/info', methods=['POST'])
def get_user_info():
    user = request.form['user_name']
    print(user)
    return jsonify({'info': f'чета поменялос'})


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
