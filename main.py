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
    return jsonify({
        '1_game_user_color': 'цвет игрока в 1 игре',
        '1_game_user_score': 'счет игрока в 1 игре',
        '1_game_user_duration': 'длительность 1 игры',
        '1_game_user_enemy_name': 'имя соперника в 1 игре',
        '1_game_user_enemy_color': 'цвет соперника в 1 игре',
        '1_game_user_enemy_score': 'счет соперника в 1 игре',
        '2_game_user_color': 'цвет игрока в 2 игре',
        '2_game_user_score': 'счет игрока в 2 игре',
        '2_game_user_duration': 'длительность 2 игры',
        '2_game_user_enemy_name': 'имя соперника в 2 игре',
        '2_game_user_enemy_color': 'цвет соперника в 2 игре',
        '2_game_user_enemy_score': 'счет соперника в 2 игре'
    }
    )

if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
