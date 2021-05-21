from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, RadioField,  PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError,  url
from wtforms.fields.html5 import URLField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Media


def rech_media():
    return Media.query.filter_by(statut=True).all()


class AjoutMediaForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    video = BooleanField()
    audio = BooleanField()
    mp_trois = FileField('mp3', validators=[FileAllowed(['mp3'],'Seul mp3 autorisé')])
    url = StringField('url')
    submit = SubmitField('Ajouter un media')


class EditMediaForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
   
    submit = SubmitField('Modifier un media')


class EditVideoForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    url = StringField('url')
    submit = SubmitField('Modifier un media')



