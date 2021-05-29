from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Rubrique


class AjoutParrainageForm(FlaskForm):
    noms= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    resume=TextAreaField('Resume', validators=[DataRequired("Completer le resumé")])
    parrainage=DecimalField('Montant')
    date_de_naissance= StringField('Date de naissance', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    image_rubrique=FileField('Image', validators=[DataRequired("Image en JPG svp "), FileAllowed(['jpg'],'Seul jpg est autorisé')])
    submit = SubmitField('Categorie')


class EditParrainageForm(FlaskForm):
    noms= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    resume=TextAreaField('Resume', validators=[DataRequired("Completer le resumé")])
    parrainage=DecimalField('Montant')
    date_de_naissance= StringField('Date de naissance', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    image_rubrique=FileField('Image', validators=[FileAllowed(['jpg'],'Seul jpg est autorisé')])
    submit = SubmitField('Categorie')

#     #Fornction de verification d'unique existenace dans la base des données
#     def validate_nom(self, nom):
#         type= Rubrique.query.filter_by(nom=nom.data).first()
#         if type:
#             raise ValidationError("Cette rubrique existe déjà")


# class EditRubForm(FlaskForm):
#     nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
#     resume=TextAreaField('Resume', validators=[DataRequired("Completer le resumé")])
#     image_rubrique=FileField('Image', validators=[FileAllowed(['jpg'],'Seul jpg est autorisé')])
#     submit = SubmitField('Categorie')


