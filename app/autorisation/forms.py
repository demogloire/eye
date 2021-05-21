from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Autorisation, User


# class AjoutAutorisationForm(FlaskForm):
#     nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
#     submit = SubmitField('Autorisation')

#     #Fornction de verification d'unique existenace dans la base des données
#     def validate_nom(self, nom):
#         type= Autorisation.query.filter_by(nom=nom.data).first()
#         if type:
#             raise ValidationError("Cette Autorisation existe déjà")

# class AjoutAssignementForm(FlaskForm):
#     nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
#     role= SelectField('Rôle',choices=[('Administrateur', 'Administrateur'), ('Webmaster', 'Webmaster')])

#     submit = SubmitField('Autorisation')

#     #Fornction de verification d'unique existenace dans la base des données
#     def validation_assignement(self, nom):
#         type= Autorisation.query.filter_by(nom=nom.data).first()
#         if type:
#             raise ValidationError("Cette Autorisation existe déjà")




