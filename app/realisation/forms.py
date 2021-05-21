from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Realisation


def rech_realisation():
    return Realisation.query.filter_by(statut=True).all()


class AjoutRealisationForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    message= TextAreaField('message', validators=[DataRequired("Completer le message")])
    date_realisation=StringField('Date', validators=[DataRequired("Entrer la date de début")])
    image_article = FileField('Image', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisé')])
    pdf_document = FileField('Image', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    lieu=StringField('Lieu', validators=[DataRequired("Entrer le lieu svp")])
    
    submit = SubmitField('Ajouter une realisation')


class EditRealisationForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    message= TextAreaField('message', validators=[DataRequired("Completer le message")])
    date_realisation=StringField('Date', validators=[DataRequired("Entrer la date de début")])
    image_article = FileField('Image', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisé')])
    pdf_document = FileField('Image', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    lieu=StringField('Lieu', validators=[DataRequired("Entrer le lieu svp")])
    
    submit = SubmitField('Ajouter une realisation')


