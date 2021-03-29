from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import redirect
from data.kgs import KGS


class AuthorizationForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    submit = SubmitField('Доступ')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pythonidory'
api = KGS("login", "password", "ru_RU")


@app.route('/', methods=['GET', 'POST'])
@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = AuthorizationForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('index.html', title='Авторизация', form=form)


@app.route('/index')
def index():
    return render_template('table.html', users=api.parse_top_100())


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
