from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Regexp, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class GameStats(FlaskForm):
    game_id = HiddenField('Game ID')
    pounds = StringField('Pounds', validators=[DataRequired(), Regexp(r'^\d*\.?\d*$', message='Please enter a valid number')])
    ounces = StringField('Ounces', validators=[DataRequired(), Regexp(r'^\d*\.?\d*$', message='Please enter a valid number')])
    length = StringField('Length', validators=[DataRequired(), Regexp(r'^\d*\.?\d*$', message='Please enter a valid number')])
    width = StringField('Width', validators=[DataRequired(), Regexp(r'^\d*\.?\d*$', message='Please enter a valid number')])
    height = StringField('Height', validators=[DataRequired(), Regexp(r'^\d*\.?\d*$', message='Please enter a valid number')])
    preset = SelectField('Preset', coerce=int, validators=[Optional()])
    update = SubmitField('Update')