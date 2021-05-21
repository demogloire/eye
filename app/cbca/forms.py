from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User

class FormCommetaire(FlaskForm):
    commmentaire= TextAreaField('Commentaire', validators=[DataRequired("Completer le commentaire")])
    submit= SubmitField('Commenter')

class FormCommetaired(FlaskForm):
    commmentaire= TextAreaField('Commentaire', validators=[DataRequired("Completer le commentaire")])
    commenter= SubmitField('Commenter')