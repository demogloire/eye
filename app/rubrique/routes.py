from flask import render_template, flash, url_for, redirect, request, session
from wtforms.fields.core import LocaleAwareNumberField
from .. import db, bcrypt
from ..models import Rubrique
from app.rubrique.forms import AjoutRubForm, EditRubForm
from app.rubrique.upload import rubrique_image
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, webmaster_admin, admin
from . import rubrique



''' Ajoute une rubrique de donation '''

@rubrique.route('/ajouter', methods=['GET','POST'])
@login_required
@admin
def ajoutrub():
   title='Rubrique'
   #formulaire
   form=AjoutRubForm()
   if form.validate_on_submit():
      nom_cat=form.nom.data
      im_phot=rubrique_image(form.image_rubrique.data)
      #Requete de verification de la rubrique
      rubrique_enre=Rubrique(nom=nom_cat, image_rubrique=im_phot, resume=form.resume.data)
      db.session.add(rubrique_enre)
      db.session.commit()
      flash("Ajout avec succès",'success')
      return redirect(url_for('rubrique.index')) 

   return render_template('rubrique/ajouter.html',  title=title, form=form)



""" Liste de catégorie """

@rubrique.route('/liste', methods=['GET', 'POST'])
@login_required
@admin
def index():
   #Titre
   title=title_page('Rubrique')
   #Requête d'affichage des rubriques
   listes=Rubrique.query.order_by(Rubrique.id.desc()).all()

   return render_template('rubrique/index.html',title=title, liste=listes)

""" Modifier statut de l'Utilisateur """
@rubrique.route('/statut/<int:rub_id>', methods=['GET', 'POST'])
@login_required
@admin
def statut(rub_id):
   #Titre
   title=title_page('Catégorie')
   #Requête de vérification de la rubrique
   cat_statu=Rubrique.query.filter_by(id=rub_id).first()

   if cat_statu is None:
      return redirect(url_for('rubrique.index'))

   if cat_statu.statut == True:
      cat_statu.statut=False
      db.session.commit()
      flash("La rubrique est désactivée sur la plateforme",'primary')
      return redirect(url_for('rubrique.index'))
   else:
      cat_statu.statut=True
      db.session.commit()
      flash("La rubrique est activée sur la plateforme",'primary')
      return redirect(url_for('rubrique.index'))
   
   return render_template('rubrique/index.html',title=title)


# """ Modification de la rubrique  """

@rubrique.route('/edit_<int:rub_id>', methods=['GET', 'POST'])
@login_required
@admin
def edit(rub_id):

   form=EditRubForm()
   #Titre
   title=title_page('Rubrique')
   #Requête de vérification du type
   rub_class=Rubrique.query.filter_by(id=rub_id).first_or_404()
   #Le nom du type encours de modification
   if form.validate_on_submit(): 
      rub_class.nom=form.nom.data
      if form.image_rubrique.data is not None:
         rub_class.image_rubrique=rubrique_image(form.image_rubrique.data)
      rub_class.resume=form.resume.data
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('rubrique.index'))
      
   if request.method=='GET':
      form.nom.data=rub_class.nom
      form.resume.data=rub_class.resume
      
   return render_template('rubrique/edit.html', form=form, title=title, image_rub=rub_class.image_rubrique)

