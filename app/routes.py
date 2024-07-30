from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, GameStats
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User, Games
from flask_login import logout_user
from flask_login import login_required
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'phil'},
            'body': 'sup'
        },
        {
            'author': {'username': 'bill'},
            'body': 'yo'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# @app.route('/manage')
# @login_required
# def manage():
#     gameForm = GameStats()
#     if request.method == 'POST':
#         game_id = request.form.get('save')
#         if game_id:
#             game = Games.query.get(game_id)
#             if game:
#                 game.pounds = float(request.form.get(f'pounds_{game.id}', 0.0))
#                 game.ounces = float(request.form.get(f'ounces_{game.id}', 0.0))
#                 game.length = float(request.form.get(f'length_{game.id}', 0.0))
#                 game.width = float(request.form.get(f'width_{game.id}', 0.0))
#                 game.height = float(request.form.get(f'height_{game.id}', 0.0))
#                 db.session.commit()
#                 flash(f'Game {game.title} updated successfully!', 'success')
#             else:
#                 flash('Game not found!', 'danger')
#         return redirect(url_for('manage'))
    
#     games = Games.query.all()
#     return render_template('manage.html', title='Site Management', games=games, form=gameForm)
@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    games = Games.query.all()
    forms = {}

    for game in games:
        form = GameStats(obj=game, prefix=str(game.id))
        forms[game.id] = form

        if form.validate_on_submit():
            form.populate_obj(game)
            db.session.commit()
            flash(f'Game {game.title} updated successfully!', 'success')
            return redirect(url_for('manage'))

    return render_template('manage.html', title='Site Management', games=games, forms=forms)
@app.route('/boxes')
@login_required
def boxes():
    return render_template('boxes.html',title="Boxes")