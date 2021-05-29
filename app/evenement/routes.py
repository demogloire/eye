import os
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Evenement
from app.evenement.forms import AjoutEvenementForm, EditEvenementForm
from app.evenement.upload import f_avatar
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import webmaster_admin,  title_page, date_modification, date_sup_ver, split_string_data, message_historique, split_string_data_form
#from slugify import slugify
from . import evenement
import timeago
from datetime import datetime, date

#Time ago
@evenement.context_processor
def utility_processor():
   def timeagos(date_time):
      date_maintenant = datetime.now()
      date_encours=timeago.format(date_maintenant, date_time , 'fr')
      return date_encours
   return dict(timeagos=timeagos)

@evenement.context_processor
def utility_processor():
   def date_french(date_sp):
      date_mois=None
      if date_sp=='01':
         date_mois='Jan'
      elif date_sp=='02':
         date_mois='Fév'
      elif date_sp=='03':
         date_mois='Mar'
      elif date_sp=='04':
         date_mois='Avr'
      elif date_sp=='05':
         date_mois='Mai'
      elif date_sp=='06':
         date_mois='Jui'
      elif date_sp=='07':
         date_mois='Juil'
      elif date_sp=='08':
         date_mois='Aoû'
      elif date_sp=='09':
         date_mois='Sep'
      elif date_sp=='10':
         date_mois='Oct'
      elif date_sp=='11':
         date_mois='Nov'
      else:
         date_mois='Déc'
      return date_mois
   return dict(date_french=date_french)

@evenement.context_processor
def utility_processor():
   def verification_date(date_1, date_2):
      date_maintenant = date.today()
      if date_1 > date_maintenant and date_2  > date_maintenant :
         return "Avant"
      elif date_1 == date_maintenant or date_maintenant <= date_2:
         return "Encours" 
      elif date_2  < date_maintenant and  date_1 < date_maintenant :
         return "Passé"
   return dict(verification_date=verification_date)   


''' Ajouter un evenement '''
@evenement.route('/ajouter', methods=['GET','POST'])
@login_required
@webmaster_admin
def ajouter():
   title=title_page('Evenement')
   #formulaire
   form=AjoutEvenementForm()

   if form.validate_on_submit():
      enreg_avatar=f_avatar(form.avatar.data)
      #date_f_debut=f_date()
      if date_sup_ver(form.date_fin.data,form.date_debut.data) is False :
         flash("Priere de verifier les dates",'primary')
         return redirect(url_for('evenement.ajouter'))
      #Enregistrement de l'evenement'
      even=Evenement(titre=form.titre.data.capitalize(), message=form.message.data, lieu=form.lieu.data, date_even=split_string_data(form.date_debut.data),
                     date_fin=split_string_data(form.date_fin.data), avatar=enreg_avatar )
      db.session.add(even)
      db.session.commit()
     
      message=f"{form.titre.data}"
      message=f"Evenement ajouté, portant sur: {form.titre.data}"
      message_historique(message=message,  user_ide=current_user.id)
      flash("L'événement est ajouté avec succès",'success')
      return redirect(url_for('evenement.index')) 

   return render_template('evenement/ajouter.html',  title=title, form=form)


@evenement.route('/', methods=['GET', 'POST'])
@login_required
@webmaster_admin
def index():

   #Titre
   title=title_page('Evenement')
   #Requête d'affichage des evenements
   listes=Evenement.query.order_by(Evenement.id.desc()).all()
   #Taille de evenements   
   taille=len(listes)

   return render_template('evenement/index.html',title=title, liste=listes, taille=taille)


@evenement.route('/edit_<int:evenement_id>_pub', methods=['GET', 'POST'])
@login_required
@webmaster_admin
def edit(evenement_id):


   form=EditEvenementForm()
   #Titre
   title=title_page('Evenement')

   pub_c=Evenement.query.filter_by(id=evenement_id).first()
   #Titre de la publication
   pub_titre=pub_c.titre

   if pub_titre is None:
      return redirect(url_for('evenement.index'))
   
   if form.validate_on_submit():
      if date_sup_ver(form.date_fin.data,form.date_even.data) is False :
         flash("Priere de verifier les dates",'primary')
         return redirect(url_for('evenement.ajouter'))

      ##Les étapes d'enregistrement des données
      pub_c.titre=form.titre.data
      pub_c.lieu=form.lieu.data
      pub_c.message=form.message.data
      if form.avatar.data is not None:
         pub_c.avatar=f_avatar(form.avatar.data) 
      pub_c.date_even=split_string_data(form.date_even.data)
      pub_c.date_fin=split_string_data(form.date_fin.data)
      db.session.commit()
      #Enregistrement
      message=f"Modification de l'evenement portant sur: {form.titre.data}"
      message_historique(message=message, user_ide=current_user.id)
      flash("Modification réussie",'success')
      return redirect(url_for('evenement.index'))
      
   if request.method=='GET':
      form.titre.data=pub_c.titre
      form.lieu.data=pub_c.lieu
      form.message.data=pub_c.message
      form.date_even.data=split_string_data_form(pub_c.date_even)
      form.date_fin.data=split_string_data_form(pub_c.date_fin)
      
   return render_template('evenement/edit.html', form=form, title=title, avatar=pub_c.avatar)

""" Modification statut """

@evenement.route('/statut/<int:evenement_id>', methods=['GET', 'POST'])
@login_required
@webmaster_admin
def statut(evenement_id): 

   #Titre
   title=title_page('Evenement')
   #Requête de vérification du type
   pub_c=Evenement.query.filter_by(id=evenement_id).first()

   if pub_c is None:
      return redirect(url_for('evenement.index'))

   if pub_c.statut == True:
      pub_c.statut=False
      db.session.commit()
      flash("Cet evenement est désactivé sur la plateforme",'primary')
      return redirect(url_for('evenement.index'))
   else:
      pub_c.statut=True
      db.session.commit()
      flash("Cet evenement est activé sur la plateforme",'primary')
      return redirect(url_for('evenement.index'))
   
   
   return render_template('evenement/index.html',title=title)
   