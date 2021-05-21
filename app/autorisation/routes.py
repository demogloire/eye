from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Autorisation, User
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page
from . import autorisation



""" Liste des Autorisations """
@autorisation.route('/', methods=['GET', 'POST'])
def index():
   #Titre
   title=title_page('Autorisation')
   #Requête de selection de toutes les données de la table autorisation
   listes=User.query.order_by(User.id.desc()).all()
   #nombre=len(listes)
   nombre=1
   if nombre >0:
      pass
   else:
      return redirect(url_for('user.ajouter'))
   return render_template('autorisation/index.html',title=title, liste=listes)


""" Modifier statut de l'activation des autorisations"""
@autorisation.route('/statut/<int:aut_id>', methods=['GET', 'POST'])
def statut(aut_id):
   #Titre
   title=title_page('Autorisation')
   #Requête de selection de toutes les données de la table autorisation filtrées par des id
   autori_statut=User.query.filter_by(id=aut_id).first()

   if autori_statut is None:
      return redirect(url_for('autorisation.index'))

   if autori_statut.statut == True:
      autori_statut.statut=False
      db.session.commit()
      flash("Cette autorisation  est désactivée sur la plateforme",'primary')
      return redirect(url_for('autorisation.index'))
   else:
      autori_statut.statut=True
      db.session.commit()
      flash("Cette autorisation est activée sur la plateforme",'primary')
      return redirect(url_for('autorisation.index'))
   
   return render_template('autorisation/index.html',title=title)
