from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Organisation, Categorie
from ..utilites.utility import message_historique
from app.authentification.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from . import auth


@auth.route('/', methods=['GET','POST'])
def login():
   #Verification de l'authentification de l'utilisateur
   if current_user.is_authenticated:
      return redirect(url_for('main.dashboard'))
   #Verification du droit d'administrateur sur la plateforme
   droit_admini_existe=User.query.filter_by(statut=True, role="Administrateur").first()
   logo=Organisation.query.first()
   cat=Categorie.query.all()
   #les rubriques
   if cat ==[]:
      liste_cat=["Actualités", "Prédications"]
      for i in liste_cat:
         enre_cat=Categorie(nom=i, statut=True)
         db.session.add(enre_cat)
         db.session.commit()
   #L'organisation
   if logo is None:
      org_o=Organisation(nom="Organisation", statut=True)
      db.session.add(org_o)
      db.session.commit()
   
   if droit_admini_existe is None:
      password_user='adminMC'
      password_hash=bcrypt.generate_password_hash(password_user).decode('utf-8') #génération du password Hacher
      #Enregistrement
      user_nv=User(nom='Admin', post_nom='Admin', prenom='Admin',\
      username='mc@mc.com', password=password_hash, password_onhash=password_user,role="Administrateur",\
      statut=True)
      db.session.add(user_nv)
      db.session.commit()
      return redirect(url_for('auth.login'))
   #Formulaire de connexion sur la plateforme
   form=LoginForm()
   #Verifiation de la connexion à l'envoie du formulaire
   if form.validate_on_submit():
      user=User.query.filter_by(username=form.username.data).first()
      ps=f'{user.prenom} {user.post_nom}'
      if user and bcrypt.check_password_hash(user.password, form.password.data):
         login_user(user, remember=form.remember.data)
         if logo is not None:
            session["nom"]=logo.nom
         else:
            session["nom"]="Organisation"
         
         message=f"Connection de {user.prenom} {user.nom} {user.post_nom}  à l'administration   "
         message_historique(message=message, user_ide=user.id)
         next_page= request.args.get('next')
         return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
      else:
         flash("Mot de passe incorrect",'danger')        
   return render_template('authentification/login.html', form=form)

#Déconnexion sur la plateforme
@auth.route("/logout")
def logout():
   message=f"Déconexion de {current_user.prenom} {current_user.nom} {current_user.post_nom}  à l'administration   "
   message_historique(message=message, user_ide=current_user.id)
   logout_user()
   return redirect(url_for('auth.login'))

