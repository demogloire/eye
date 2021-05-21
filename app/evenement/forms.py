from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Evenement


def rech_evenement():
    return Evenement.query.filter_by(statut=True).all()


class AjoutEvenementForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    lieu= StringField('Lieu', validators=[DataRequired("Completer le lieu")])
    message= TextAreaField('message', validators=[DataRequired("Completer le message")])
    date_debut=StringField('Date de debut', validators=[DataRequired("Entrer la date de début")])
    date_fin=StringField('Date de fin', validators=[DataRequired("Entrer la date de fin")])
    avatar=FileField("Selectionner une photo", validators=[FileAllowed(['png','jpg','gif'],'Seules les photos png, jpg et gif sont autorisés')])

    submit = SubmitField('Ajouter un evenment')


class EditEvenementForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    lieu= StringField('Lieu', validators=[DataRequired("Completer le lieu")])
    message= TextAreaField('message', validators=[DataRequired("Completer le message")])
    date_even=StringField('Date de debut', validators=[DataRequired("Entrer la date de début")])
    date_fin=StringField('Date de fin', validators=[DataRequired("Entrer la date de fin")])
    avatar=FileField("Selectionner une photo", validators=[FileAllowed(['png','jpg','gif'],'Seules les photos png, jpg et gif sont autorisés')])


    submit = SubmitField('Modifier un evenment')


