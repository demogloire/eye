from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Realisation


def rech_realisation():
    return Realisation.query.filter_by(statut=True).all()


class AjoutOrganisationForm(FlaskForm):
    nom= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères"), ])
    adresse_mail= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères"), Email('Votre email est incorrect')])
    adresse_physique= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    personnalite_juridique= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    num_telephone= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    logo=FileField("Selectionner une photo", validators=[FileAllowed(['png','jpg','gif'],'Seules les photos png, jpg et gif sont autorisés')])
    submit = SubmitField('Ajouter une Organisation')


class EditOrganisationForm(FlaskForm):
    nom= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    adresse_mail= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    adresse_physique= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    personnalite_juridique= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    num_telephone= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    logo=FileField("Selectionner une photo", validators=[FileAllowed(['png','jpg','gif'],'Seules les photos png, jpg et gif sont autorisés')])

    submit = SubmitField('Modifier une organisation')


