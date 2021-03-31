from flask import Flask, render_template, request, jsonify
from data.kgs import KGS

app = Flask(__name__)
api = KGS("pamparam", "i7deu8", "ru_RU")
REQUESTED = []


@app.route('/')
@app.route('/table')
def index():
    return render_template('table.html', users=api.parse_top_100())


@app.route('/info', methods=['POST'])
def get_user_info():
    user = request.form['user_name']
    if user not in REQUESTED:
        REQUESTED.append(user)
        arh_join = KGS.get_typed(api.join_archive_request(user)["messages"], "ARCHIVE_JOIN")

        lobby1 = KGS.get_typed(
            api.room_load_game(arh_join["games"][-1]["timestamp"], 22)["messages"],
            "GAME_JOIN")
        lobby2 = KGS.get_typed(
            api.room_load_game(arh_join["games"][-2]["timestamp"], 22)["messages"],
            "GAME_JOIN")

        players_1 = list(enumerate(KGS.get_players(arh_join, -1)))
        game_1 = {'num': '1',
                  'duration': KGS.get_duration(lobby1),
                  'score': KGS.get_score(arh_join, -1),
                  'users_amount': len(players_1),
                  'users': [{'name': name,
                             'color': KGS.get_colors(arh_join, -1)[i]}
                            for i, name in players_1]
                  }
        players_2 = list(enumerate(KGS.get_players(arh_join, -2)))
        game_2 = {'num': '2',
                  'duration': KGS.get_duration(lobby2),
                  'score': KGS.get_score(arh_join, -2),
                  'users_amount': len(players_2),
                  'users': [{'name': name,
                             'color': KGS.get_colors(arh_join, -2)[i]}
                            for i, name in players_2]
                  }

        games_json = jsonify({'games': [game_1, game_2]})
        return games_json
    return jsonify({'success': 'OK'})


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
