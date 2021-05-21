from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Categorie


def rech_categorie():
    return Categorie.query.filter_by(statut=True).all()


class AjoutPubForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    resume= TextAreaField('Resume', validators=[DataRequired("Completer le resumé")])
    categorie= QuerySelectField(query_factory=rech_categorie, get_label='nom', allow_blank=False)
    image_article = FileField('Image', validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisé')])
    pdf_document = FileField('Image', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    url = StringField('url')
    submit = SubmitField('Ajouter publication')


class EditPubForm(FlaskForm):
    titre= StringField('Titre', validators=[DataRequired("Completer le titre"),  Length(min=2, max=255, message="Veuillez respecté les caractères")])
    resume= TextAreaField('Resume', validators=[DataRequired("Completer le resumé")])
    url = StringField('url')
    categorie= QuerySelectField(query_factory=rech_categorie, get_label='nom', allow_blank=False)
    submit = SubmitField('Ajouter publication')


class AjMediaForm(FlaskForm):
    image_article = FileField('Image', validators=[FileAllowed(['jpg','png'],'Seul jpg est autorisé')])
    submit = SubmitField('Publier')

class AjPDFForm(FlaskForm):
    image_article = FileField('Image', validators=[FileAllowed(['pdf'],'Seul pdf est autorisé')])
    submit = SubmitField('Publier')

