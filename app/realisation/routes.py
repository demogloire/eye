import os
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Realisation
from app.realisation.forms import AjoutRealisationForm, EditRealisationForm
from app.realisation.upload import f_avatar, publication_doc, save_image_mod
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, date_modification, date_sup_ver, split_string_data, message_historique, split_string_data_form
#from slugify import slugify
from . import realisation
import timeago
from datetime import datetime, date

@realisation.context_processor
def utility_processor():
   def moisan(date_real):
      date_real=str(date_real)
      date_realisation=date_real.split('-')
      mois_an="{}/{}".format(date_realisation[1],date_realisation[0])
      return mois_an
   return dict(moisan=moisan)

@realisation.context_processor
def utility_processor():
   def timeagos(date_time):
      date_maintenant = datetime.now()
      date_encours=timeago.format(date_maintenant, date_time , 'fr')
      return date_encours
   return dict(timeagos=timeagos)

''' Ajouter une realisation '''
@realisation.route('/ajouter', methods=['GET','POST'])
@login_required
def ajouter():
   title=title_page('Réalisation')
   #formulaire
   form=AjoutRealisationForm()

   
   if form.validate_on_submit():

      if form.image_article.data is not None or form.pdf_document.data is not None:
         if form.image_article.data is not None  and form.pdf_document.data is None:
            image=publication_doc(form.image_article.data)
            #Enregistrement de la realisation'
            enreg_realisation=Realisation(titre=form.titre.data, message=form.message.data, 
                                          image_article=image,lieu=form.lieu.data, date_realisation=split_string_data(form.date_realisation.data))
            
         elif form.image_article.data is not None  and form.pdf_document.data is not None:
            pdf=publication_doc(form.pdf_document.data)
            image=publication_doc(form.image_article.data)
            #Enregistrement de la realisation'
            enreg_realisation=Realisation(titre=form.titre.data, message=form.message.data, 
                                          image_article=image, pdf_document=pdf,lieu=form.lieu.data, date_realisation=split_string_data(form.date_realisation.data))    

         else:
            flash("Ajouter une image de la réalisation svp ",'danger')
            return redirect(url_for('realisation.ajouter'))          
         
         db.session.add(enreg_realisation)
         db.session.commit()
         message=f"{form.titre.data}"
         message=f"Realisation ajouté, portant sur:{form.titre.data}"
         message_historique(message, user_ide=current_user.id)
         flash("Ajout réussie",'success')
         return redirect(url_for('realisation.index')) 
      else:
         flash("Attention ajouter soit une image ou un document",'danger')
         return redirect(url_for('realisation.ajouter')) 
             
   if request.method=='GET':
      form.date_realisation.data=split_string_data_form(date.today())

   return render_template('realisation/ajouter.html',  title=title, form=form)


@realisation.route('/', methods=['GET', 'POST'])
def index():

   #Titre
   title=title_page('Réalisation')
   #Liste des publications
   page= request.args.get('page', 1, type=int)
   #Requête d'affichage des realisations
   listes=Realisation.query.order_by(Realisation.id.desc()).paginate(page=page, per_page=4)
   #Taille de Realisations  
   taille=len(listes.items)

   return render_template('realisation/index.html',title=title, liste=listes, taille=taille)


@realisation.route('/edit_<int:realisation_id>_pub', methods=['GET', 'POST'])
def edit(realisation_id):


   form=EditRealisationForm()
   #Titre
   title=title_page('Réalisation')

   pub_c = Realisation.query.filter_by(id=realisation_id).first()
   #Envoie des données
   pdf=None
   image=None
   
   if form.validate_on_submit():
      #Mise à jour des documents
      if form.pdf_document.data is not None:
         pdf=save_image_mod(form.pdf_document.data, pub_c.pdf_document )
      else:
         pdf=pub_c.pdf_document
         
      if form.image_article.data is not None:
         image=save_image_mod(form.image_article.data,pub_c.image_article)
      else:
         image=pub_c.image_article
      #Mise à jour des données
      pub_c.titre=form.titre.data
      pub_c.message=form.message.data
      pub_c.date_realisation=split_string_data(form.date_realisation.data)
      pub_c.image_article=image
      pub_c.pdf_document=pdf
      pub_c.lieu=form.lieu.data
      db.session.commit()
      #Enregistrement
      message=f"Modification de la realisation portant sur:{form.titre.data}"
      message_historique(message, user_ide=current_user.id)

      flash("Modification réussie",'success')
      return redirect(url_for('realisation.index'))
      
   if request.method=='GET':
      form.titre.data=pub_c.titre
      form.message.data=pub_c.message
      form.lieu.data=pub_c.lieu
      form.date_realisation.data=split_string_data_form(pub_c.date_realisation)

   return render_template('realisation/edit.html', form=form, title=title)

""" Modification statut """

@realisation.route('/statut/<int:realisation_id>', methods=['GET', 'POST'])
def statut(realisation_id): 

   #Titre
   title=title_page('Réalisation')
   #Requête de vérification du type
   pub_c=Realisation.query.filter_by(id=realisation_id).first()

   if pub_c is None:
      return redirect(url_for('realisation.index'))

   if pub_c.statut == True:
      pub_c.statut=False
      db.session.commit()
      flash("Cette realisation est désactivée sur la plateforme",'success')
      return redirect(url_for('realisation.index'))
   else:
      pub_c.statut=True
      db.session.commit()
      flash("Cette realisation est activée sur la plateforme",'success')
      return redirect(url_for('realisation.index'))
   
   
   return render_template('realisation/index.html',title=title)
   