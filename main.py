from flask import Flask, render_template, request, jsonify
from data.kgs import KGS

app = Flask(__name__)
api = KGS("pamparam", "i7deu8", "ru_RU")
REQUESTED = []


@app.route('/')
@app.route('/table')
def index():
    return render_template('table.html', users=api.parse_top_100())


@app.route('/match_replay')
def replay():
    return render_template('match_replay.html', size_table=19)


@app.route('/info', methods=['POST'])
def get_user_info():
    user = request.form['user_name']
    if user not in REQUESTED:
        REQUESTED.append(user)
        arh_join = KGS.get_typed(api.join_archive_request(user)["messages"], "ARCHIVE_JOIN")
        a = api.room_load_game(arh_join["games"][-1]["timestamp"], 22)["messages"]
        lobby1 = KGS.get_typed(
            api.room_load_game(arh_join["games"][-1]["timestamp"], 22)["messages"],
            "GAME_JOIN")
        b = api.room_load_game(arh_join["games"][-2]["timestamp"], 22)["messages"]
        lobby2 = KGS.get_typed(
            api.room_load_game(arh_join["games"][-2]["timestamp"], 22)["messages"],
            "GAME_JOIN")
        print(a, b, sep='\n')

        return jsonify({
            '1_game_user_color': KGS.get_colors(arh_join, -1)[0],
            '1_game_user_score': KGS.get_score(arh_join, -1),
            '1_game_user_duration': KGS.get_duration(lobby1),
            '1_game_user_enemy_name': KGS.get_players(arh_join, -1)[1],
            '1_game_user_enemy_color': KGS.get_colors(arh_join, -1)[1],
            '1_game_user_enemy_score': KGS.get_score(arh_join, -1),
            '2_game_user_color': KGS.get_colors(arh_join, -2)[0],
            '2_game_user_score': KGS.get_score(arh_join, -2),
            '2_game_user_duration': KGS.get_duration(lobby2),
            '2_game_user_enemy_name': KGS.get_players(arh_join, -2)[1],
            '2_game_user_enemy_color': KGS.get_colors(arh_join, -2)[1],
            '2_game_user_enemy_score': KGS.get_score(arh_join, -2)
        }
        )


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')