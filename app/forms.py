from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class GameStats(FlaskForm):
    game_id = HiddenField('Game ID')
    pounds = DecimalField('Pounds', validators=[DataRequired()])
    ounces = DecimalField('Ounces', validators=[DataRequired()])
    length = DecimalField('Length', validators=[DataRequired()])
    width = DecimalField('Width', validators=[DataRequired()])
    height = DecimalField('Height', validators=[DataRequired()])
    update = SubmitField('Update')