from pprint import pprint

from flask import Flask, render_template, request, jsonify
from data.kgs import KGS

app = Flask(__name__)
api = KGS("pamparam", "i7deu8", "ru_RU")
REQUESTED = []


@app.route('/')
@app.route('/leaderboard')
def index():
    return render_template('table.html', users=api.parse_top_100())


@app.route('/info', methods=['POST'])
def get_user_info():
    user = request.form['user_name']
    if user not in REQUESTED:
        REQUESTED.append(user)
        arh_join = KGS.get_typed(api.join_archive_request(user)["messages"], "ARCHIVE_JOIN")

        lobby1 = api.get_lobby(arh_join, -1)
        lobby2 = api.get_lobby(arh_join, -2)

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

        games_json = jsonify({'games': [game_1, game_2], 'success': 'OK'})
        return games_json


@app.route('/leaderboard/review/<string:user>/<string:game_num>')
def game_review(user, game_num):
    print(api.get_game_moves(user, int(game_num)))


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
