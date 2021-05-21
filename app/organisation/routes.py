import os
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Organisation, Historique
from app.organisation.forms import AjoutOrganisationForm, EditOrganisationForm
from app.organisation.upload import f_avatar, publication_doc, save_image_mod
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import webmaster_admin, admin, title_page, date_modification, date_sup_ver, split_string_data, message_historique
#from slugify import slugify
from . import organisation
import timeago
from datetime import datetime


@organisation.context_processor
def utility_processor():
   def timeagos(date_time):
      date_maintenant = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      date_encours=timeago.format(date_time,date_maintenant,'fr')
      return date_encours
   return dict(timeagos=timeagos)

''' Ajouter une organisation '''
@organisation.route('/ajouter', methods=['GET','POST'])
@login_required
@admin
def ajouter():
   title=title_page('Organisation')
   #formulaire
   form=AjoutOrganisationForm()
   #Existence des informations de l'organisation
   org=Organisation.query.first()
   if org is not None:
      return redirect(url_for('main.dashboard'))

   if form.validate_on_submit():
      enreg_logo=publication_doc(form.logo.data)
      #Enregistrement de l'organisation
      enreg_org=Organisation(nom=form.nom.data.capitalize(), adresse_mail=form.adresse_mail.data, 
                                 personnalite_juridique=form.personnalite_juridique.data, adresse_physique=form.adresse_physique.data,num_telephone=form.num_telephone.data, logo=enreg_logo )
      db.session.add(enreg_org)
      db.session.commit()
   
      message=f"{form.nom.data}"
      message=f"Ajout des informations de l'organisation avec le nom: {form.nom.data}"
      message_historique(message, user_ide=current_user.id)
      return redirect(url_for('organisation.index')) 

   return render_template('organisation/ajouter.html',  title=title, form=form)


@organisation.route('/<int:id_pro>/<int:id_act>', methods=['GET', 'POST'])
@login_required
@admin
def index(id_pro,id_act):
   #Titre
   title=title_page('Organisation')
   #Requête d'affichage des organisations
   controle_pro=0
   controle_act=0
   if id_pro==1:
      controle_pro=1
   else:
      controle_pro=0
   #Variable de controle
   if id_act==1:
          controle_act=1
   else:
      controle_act=0
   
   #Nombre d'organisation en cours
   listes=Organisation.query.first()
   controle_org=None
   if listes is None:
      controle_org=0
   else:
      controle_org=1
   
   page= request.args.get('page', 1, type=int)
   activites=Historique.query.order_by(Historique.id.desc()).paginate(page=page, per_page=30)
   
   
   return render_template('organisation/index.html',title=title,activites=activites,liste=listes,controle_act=controle_act,controle_pro=controle_pro, controle_org=controle_org)


@organisation.route('/edit_<int:organisation_id>', methods=['GET', 'POST'])
@login_required
@admin
def edit(organisation_id):

   form=EditOrganisationForm()
   #Titre
   title=title_page('Organisation')

   pub_c = Organisation.query.filter_by(id=organisation_id).first()
   #Envoie des données
   
   if form.validate_on_submit():
      logo=None
      if form.logo.data is not None:
         logo=save_image_mod(form.logo.data, pub_c.logo) 
      else:
         logo=pub_c.logo
      pub_c.nom= form.nom.data
      pub_c.adresse_mail=form.adresse_mail.data
      pub_c.personnalite_juridique=form.personnalite_juridique.data
      pub_c.num_telephone=form.num_telephone.data
      pub_c.adresse_physique=form.adresse_physique.data
      pub_c.logo=logo
      db.session.commit()
      #Enregistrement
      message=f"Modification des informations de l'orgnisation par {current_user.prenom} {current_user.nom} {current_user.post_nom}"
      message_historique(message=message, user_ide=current_user.id)
      flash("Modification réussie",'success')
      return redirect(url_for('organisation.index',id_pro=1,id_act=0))
      
   if request.method=='GET':
     form.nom.data=pub_c.nom
     form.adresse_mail.data =pub_c.adresse_mail
     form.personnalite_juridique.data=pub_c.personnalite_juridique
     form.adresse_physique.data=pub_c.adresse_physique
     form.num_telephone.data=pub_c.num_telephone

   return render_template('organisation/edit.html', form=form, title=title)

""" Modification statut """

@organisation.route('/statut/<int:organisation_id>', methods=['GET', 'POST'])
@login_required
@admin
def statut(organisation_id): 

   #Titre
   title=title_page('Organisation')
   #Requête de vérification du type
   pub_c=Organisation.query.filter_by(id=organisation_id).first()

   if pub_c is None:
      return redirect(url_for('organisation.index'))

   if pub_c.statut == True:
      pub_c.statut=False
      db.session.commit()
      flash("Cette organisation est désactivée sur la plateforme",'primary')
      return redirect(url_for('organisation.index'))
   else:
      pub_c.statut=True
      db.session.commit()
      flash("Cette organisation est activée sur la plateforme",'primary')
      return redirect(url_for('organisation.index'))
   
   
   return render_template('organisation/index.html',title=title)
   