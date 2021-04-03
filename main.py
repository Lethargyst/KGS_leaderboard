from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

from data.kgs import KGS
from data.GameReview import Reviewer


class AuthorizationForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    submit = SubmitField('Войти')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pythonidory'
API = KGS("ilushandr", "527fqe", "ru_RU")
REQUESTED = []
REVIEWER = Reviewer()


@app.route('/', methods=['GET', 'POST'])
def authorization():
    form = AuthorizationForm()
    if form.validate_on_submit():
        return redirect('/leaderboard')
    return render_template('autho.html', title='Авторизация', form=form)


@app.route('/leaderboard')
def leaderboard():
    return render_template('table.html', users=API.parse_top_100())


@app.route('/info', methods=['POST'])
def get_user_info():
    user = request.form['user_name']
    if user not in REQUESTED:
        API.login("ilushandr", "527fqe", "ru_RU")
        arh_join = KGS.get_typed(API.join_archive_request(user)["messages"], "ARCHIVE_JOIN")

        lobby1 = API.get_lobby(arh_join, -1)
        lobby2 = API.get_lobby(arh_join, -2)

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
        REQUESTED.append(user)
        return games_json


@app.route('/leaderboard/review/<string:user>/<string:game_num>')
def game_review(user, game_num):
    API.login("ilushandr", "527fqe", "ru_RU")
    REVIEWER.init_match(*API.get_game_params(user, int(game_num)))
    return render_template('match_review.html')


@app.route('/review_rendering', methods=['POST'])
def render_board():
    iteration = int(request.form['iteration'])
    action = request.form['action']
    if action == '+':
        iteration += 1
    else:
        iteration -= 1
    REVIEWER.render_iteration(iteration)

    return jsonify({'src': f'/static/img/board.png', 'iteration': str(iteration)})


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')