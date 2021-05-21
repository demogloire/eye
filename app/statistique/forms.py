from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import User

class RechercheForm(FlaskForm):
    mois= StringField('Date mensuelle')
    annee= StringField('Annuelle')
    submit = SubmitField('Connexion')

    def validate_annee(self, annee):
        d=annee.data
        if d !='':
            try:
                annee_op=int(annee.data)
            except :
                raise ValidationError("L'année doit être de chiffre supieur à 2000")

            if annee_op > 2000:
                pass
            else:
                raise ValidationError("L'année doit être superieur à 2000")

      