from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User, Rubrique

def rech_rubrique():
    return Rubrique.query.filter_by(statut=True).all()


class FormCommetaire(FlaskForm):
    commmentaire= TextAreaField('Commentaire', validators=[DataRequired("Completer le commentaire")])
    submit= SubmitField('Commenter')

class FormCommetaired(FlaskForm):
    commmentaire= TextAreaField('Commentaire', validators=[DataRequired("Completer le commentaire")])
    commenter= SubmitField('Commenter')
    
class FormDonation(FlaskForm):
    noms= StringField('Lieu', validators=[DataRequired("Nom")])
    adresse_mail= StringField('Lieu', validators=[DataRequired("Votre adresse mail"), Email('Votre email est incorrect')])
    montant=IntegerField('montant')
    #montant = SelectField(u'Choice amount', choices=[(5, '5 USD'), (10, '10 USD'), (20 , '20 USD')])
    cause= QuerySelectField(query_factory=rech_rubrique, get_label='nom', allow_blank=False)
    submit = SubmitField('Ajouter donation')