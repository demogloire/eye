from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User


class AjoutUserForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer le nom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    post_nom= StringField('Post-Nom', validators=[DataRequired("Completer le post-nom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    prenom= StringField('Prénom', validators=[DataRequired("Completer le prenom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    email= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    password= PasswordField('Mot de passe', validators=[DataRequired("Completer votre mot de passe"),  Length(min=6, max=13, message="Veuillez respecté les caractères")])
    confirm_password= PasswordField('Confirmer mot de passe', validators=[DataRequired('Veuillez completer votre mot de passe'), EqualTo('password')])
    role= SelectField('Rôle',choices=[('Administrateur', 'Administrateur'), ('Webmaster', 'Webmaster')])

    submit = SubmitField('Ajouter user')

        #Foction de la verification d'unique existencce dans la base des données
    def validate_email(self, email):
        user=User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError("Cet utilisateur existe déjà")

class EditUserForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer le nom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    post_nom= StringField('Post-Nom', validators=[DataRequired("Completer le post-nom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    prenom= StringField('Prénom', validators=[DataRequired("Completer le prenom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    role= SelectField('Rôle',choices=[('Administrateur', 'Administrateur'), ('Webmaster', 'Webmaster')])
    email= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    password= PasswordField('Mot de passe')
    submit = SubmitField('Ajouter user')

class EditProfilForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer le nom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    post_nom= StringField('Post-Nom', validators=[DataRequired("Completer le post-nom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    prenom= StringField('Prénom', validators=[DataRequired("Completer le prenom"),  Length(min=2, max=200, message="Veuillez respecté les caractères")])
    email= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    password= PasswordField('Mot de passe')
    submit = SubmitField('Ajouter user')


