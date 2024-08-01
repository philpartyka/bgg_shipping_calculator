from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, GameStats
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import app, db
from app.models import User, Games, GamePreset
from flask_login import logout_user
from flask_login import login_required
from urllib.parse import urlsplit

def format_number(value):
    try:
        # Convert to float and format with 2 decimal places
        formatted = '{:.2f}'.format(float(value))
        # Remove trailing zeros, but keep one zero after decimal point if needed
        formatted = formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
        return formatted
    except ValueError:
        return value  # Return original value if conversion fails
    
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
@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    app.jinja_env.filters['format_number'] = format_number
    games = Games.query.all()
    presets = GamePreset.query.all()
    forms = {}

    for game in games:
        form = GameStats(obj=game, prefix=str(game.id))
        form.preset.choices = [
            (0, 'Select preset')
        ] + [
            (p.id, f"{p.name} ({p.length}x{p.width}x{p.height})") 
            for p in presets
        ]
        forms[game.id] = form

        if form.validate_on_submit():
            form.populate_obj(game)
            if form.preset.data and form.preset.data != 0:
                preset = GamePreset.query.get(form.preset.data)
                if preset:
                    game.length = preset.length
                    game.width = preset.width
                    game.height = preset.height
            db.session.commit()
            flash(f'Game {game.title} updated successfully!', 'success')
            return redirect(url_for('manage'))

    return render_template('manage.html', title='Site Management', games=games, forms=forms)

@app.route('/get_preset/<int:preset_id>')
def get_preset(preset_id):
    preset = GamePreset.query.get_or_404(preset_id)
    return jsonify({
        'length': preset.length,
        'width': preset.width,
        'height': preset.height
    })
@app.route('/boxes')
@login_required
def boxes():
    return render_template('boxes.html',title="Boxes")