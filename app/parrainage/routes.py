from flask import render_template, flash, url_for, redirect, request, session
from wtforms.fields.core import LocaleAwareNumberField
from .. import db, bcrypt
from ..models import Parrainage
from app.parrainage.forms import AjoutParrainageForm, EditParrainageForm
from datetime import datetime, date
from app.parrainage.upload import rubrique_image
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, webmaster_admin, admin, split_string_data, split_string_data_form
from . import parrainage




#Time ago
@parrainage.context_processor
def utility_processor():
   def age_naissance(date_time):
      today = date.today()
      age = today.year - date_time.year - ((today.month, today.day) < (date_time.month, date_time.day))
      print(today, date_time,  age,'dddddddddddddddddddddddddddddddddddddddddddddddddddd')
      return age
   return dict(age_naissance=age_naissance)


''' Ajoute à parrainer '''

@parrainage.route('/ajouter/enfant', methods=['GET','POST'])
@login_required
@admin
def ajouter():
   title='Parrainage'
   #formulaire
   form=AjoutParrainageForm()
   if form.validate_on_submit():
      nom_cat=form.noms.data
      im_phot=rubrique_image(form.image_rubrique.data)
      #Requete de verification de la rubrique
      enfant_enre=Parrainage(noms=nom_cat, image_rubrique=im_phot, resume=form.resume.data, parrainage=form.parrainage.data, date_de_naissance=split_string_data(form.date_de_naissance.data), statut=True)
      db.session.add(enfant_enre)
      db.session.commit()
      flash("Ajout de l'enfant avec succès",'success')
      return redirect(url_for('parrainage.index')) 

   return render_template('parrainage/ajouter.html',  title=title, form=form)



""" Liste des enfants """

@parrainage.route('/liste', methods=['GET', 'POST'])
@login_required
@admin
def index():
   #Titre
   title=title_page('Parrainage')
   #Requête d'affichage des rubriques
   listes=Parrainage.query.order_by(Parrainage.id.desc()).all()

   return render_template('parrainage/index.html',title=title, liste=listes)

""" Modifier statut de l'enfant """

@parrainage.route('/statut/<int:enf_id>', methods=['GET', 'POST'])
@login_required
@admin
def statut(enf_id):
   #Titre
   title=title_page('Parrainage')
   #Requête de vérification d'enfant
   enfant_statu=Parrainage.query.filter_by(id=enf_id).first()

   if enfant_statu is None:
      return redirect(url_for('parrainage.index'))

   if enfant_statu.statut == True:
      enfant_statu.statut=False
      db.session.commit()
      flash("L'enfant est désactivé sur le parrainage",'primary')
      return redirect(url_for('parrainage.index'))
   else:
      enfant_statu.statut=True
      db.session.commit()
      flash("L'enfant est activé sur le parrainage",'primary')
      return redirect(url_for('parrainage.index'))
   
   return render_template('parrainage/index.html',title=title)


# """ Modification de la parrainage  """

@parrainage.route('/edit_<int:enf_id>', methods=['GET', 'POST'])
@login_required
@admin
def edit(enf_id):

   form=EditParrainageForm()
   #Titre
   title=title_page('Parrainage')
   #Requête de vérification du type
   enfant_class=Parrainage.query.filter_by(id=enf_id).first_or_404()
   #Le nom du type encours de modification
   if form.validate_on_submit(): 
      enfant_class.noms=form.noms.data
      if form.image_rubrique.data is not None:
         enfant_class.image_rubrique=rubrique_image(form.image_rubrique.data)
      enfant_class.resume=form.resume.data
      enfant_class.date_de_naissance=split_string_data(form.date_de_naissance.data)
      enfant_class.parrainage=form.parrainage.data
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('parrainage.index'))
      
   if request.method=='GET':
      form.noms.data=enfant_class.noms
      form.resume.data=enfant_class.resume
      form.parrainage.data=enfant_class.parrainage
      form.date_de_naissance.data=split_string_data_form(enfant_class.date_de_naissance)
      
   return render_template('parrainage/edit.html', form=form, title=title, image_rub=enfant_class.image_rubrique)

