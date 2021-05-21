from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User, Historique
from app.user.forms import AjoutUserForm, EditUserForm, EditProfilForm
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, message_historique, webmaster_admin, admin
from . import user
import timeago
from datetime import datetime


@user.context_processor
def utility_processor():
   def timeagos(date_time):
      date_maintenant = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      date_encours=timeago.format(date_time,date_maintenant,'fr')
      return date_encours
   return dict(timeagos=timeagos)

""" Ajout utilisateur"""
@user.route('/ajouter', methods=['GET','POST'])
@login_required
@admin
def ajouter():
   #Un utilisateur
   form=AjoutUserForm()
   #Titre de l'onglet
   title=title_page("Utilisateur")

   if form.validate_on_submit():
      password_user=form.password.data
      password_hash=bcrypt.generate_password_hash(password_user).decode('utf-8') #génération du password Hacher
      #Enregistrement
      user_nv=User(nom=form.nom.data.upper(), post_nom=form.post_nom.data.upper(), prenom=form.prenom.data.capitalize(),\
      username=form.email.data, password=password_hash, password_onhash=password_user,role=form.role.data,\
      statut=True)
      db.session.add(user_nv)
      db.session.commit()
      message=f"Ajout de l'utilisateur {form.prenom.data.capitalize()} {form.nom.data.upper()} {form.post_nom.data.upper()} ayant comme rôle {form.role.data} "
      message_historique(message=message, user_ide=user_nv.id)
      flash("Ajout avec success",'success')
      return redirect(url_for('user.index'))
         
   return render_template('user/ajouter.html', form=form, title=title)


""" Liste des utilisateurs """
@user.route('/', methods=['GET', 'POST'])
@login_required
@admin
def index():
   #Titre
   title=title_page("Utilisateur")
   #Requête d'affichage des utilisateurs
   listes=User.query.order_by(User.id.desc()).all()
   return render_template('user/index.html',title=title, liste=listes)


""" Statut"""
@user.route('/statut/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin
def statut(user_id):
   #Titre
   title=title_page('Catégorie')
   #Requête de vérification de l'utilisateur
   user_statu=User.query.filter_by(id=user_id).first()
   if current_user.id == user_statu.id:
      flash("C'est un utilisateur connecté".format(current_user.prenom),'danger')
      return redirect(url_for('user.index'))
   
   if user_statu is None:
      return redirect(url_for('user.index'))
   if user_statu.statut == True:
      user_statu.statut=False
      db.session.commit()
      message=f"Désactivation de l'utilisateur {user_statu.prenom} {user_statu.nom} {user_statu.post_nom}"
      message_historique(message=message, user_ide=user_statu.id)
      flash("{} est désactivé".format(user_statu.prenom),'primary')
      return redirect(url_for('user.index'))
   else:
      user_statu.statut=True
      db.session.commit()
      message=f"Activation de l'utilisateur {user_statu.prenom} {user_statu.nom} {user_statu.post_nom}"
      message_historique(message=message, user_ide=user_statu.id)
      flash("{} est activé".format(user_statu.prenom),'success')
      return redirect(url_for('categorie.index'))
   
   return render_template('user/index.html',title=title)


""" Modifier"""
@user.route('/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin
def edit(user_id):
   form=EditUserForm()
   #Titre
   title=title_page('Utilisateur')
   #Requête de vérification de l'utlisateur
   user_class=User.query.filter_by(id=user_id).first()
   #Le nom du type encours de modification
   user_nom=user_class.prenom

   if user_nom is None:
      return redirect(url_for('user.index'))
   
   if form.validate_on_submit(): 
      mail=None
      password=None
      if form.email.data ==user_class.username:
         mail=user_class.username
      else:
         user_ver=User.query.filter_by(username=form.email.data).first()
         if user_ver is not None:
            flash("Cet utilisateur existe déjà",'danger')
            return redirect(url_for('user.edit', user_id=user_class.id))
         else:
            mail=form.email.data
            
      if form.password.data!='':
        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      else:
         password=user_class.password
      
      user_class.nom=form.nom.data.upper()
      user_class.username=mail
      user_class.password=password
      user_class.post_nom=form.post_nom.data.upper()
      user_class.prenom=form.prenom.data.capitalize()
      user_class.role=form.role.data
      db.session.commit()
      message=f"Modification des informations de {user_class.prenom} {user_class.nom} {user_class.post_nom} par {current_user.prenom} "
      message_historique(message=message, user_ide=user_class.id)
      flash("Modification réussie",'success')
      return redirect(url_for('user.index'))
      
   if request.method=='GET':
      form.nom.data=user_class.nom
      form.email.data=user_class.username
      form.post_nom.data=user_class.post_nom
      form.prenom.data=user_class.prenom
      form.role.data=user_class.role
      
   return render_template('user/edit.html', form=form, title=title, user_nom=user_nom)


""" Modifier sur profil utilisateur"""
@user.route('/profil/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin
def edit_profil(user_id):
   form=EditProfilForm()
   #Titre
   title=title_page('Utilisateur')
   #Requête de vérification de l'utlisateur
   user_class=User.query.filter_by(id=user_id).first_or_404()
   #Le nom du type encours de modification
   user_nom=user_class.prenom
   if user_nom is None:
      return redirect(url_for('user.index'))
   
   if user_id!=current_user.id:
      return redirect(url_for('main.dashboard'))
   
   if form.validate_on_submit(): 
      mail=None
      password=None
      if form.email.data ==user_class.username:
         mail=user_class.username
      else:
         user_ver=User.query.filter_by(username=form.email.data).first()
         if user_ver is not None:
            flash("Cet utilisateur existe déjà",'danger')
            return redirect(url_for('user.edit', user_id=user_class.id))
         else:
            mail=form.email.data
            
      if form.password.data!='':
        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      else:
         password=user_class.password
      
      user_class.nom=form.nom.data.upper()
      user_class.username=mail
      user_class.password=password
      user_class.post_nom=form.post_nom.data.upper()
      user_class.prenom=form.prenom.data.capitalize()
      db.session.commit()
      message=f"Modification des informations de {user_class.prenom} {user_class.nom} {user_class.post_nom} par lui-même {current_user.prenom} "
      message_historique(message=message, user_ide=current_user.id)
      flash("Modification réussie",'success')
      return redirect(url_for('user.profil',id_pro=1, id_act=0, user_id=current_user.id))
      
   if request.method=='GET':
      form.nom.data=user_class.nom
      form.email.data=user_class.username
      form.post_nom.data=user_class.post_nom
      form.prenom.data=user_class.prenom

      
   return render_template('user/edit_profil.html', form=form, title=title,user_id=user_class.id, user_nom=user_nom, id_pro=1, id_act=0)


""" Modifier sur profil utilisateur"""
@user.route('/<int:user_id>/<int:id_act>/<int:id_pro>/profil', methods=['GET', 'POST'])
@login_required
def profil(user_id, id_act, id_pro):
   #Requête d'affichage des organisations
   
   controle_pro=0
   controle_act=0
   #Variable de controle
   if id_act==1:
          controle_act=1
   else:
      controle_act=0
   
   if id_pro==1:
      controle_pro=1
   else:
      controle_pro=0
   
   if user_id !=current_user.id:
      return redirect(url_for('main.dashboard'))
       
   #Nombre d'organisation en cours
   listes=User.query.filter_by(id=user_id).first_or_404()
   page= request.args.get('page', 1, type=int)
   activites=Historique.query.filter_by(user_id=user_id).order_by(Historique.id.desc()).paginate(page=page, per_page=30)
  
      
   return render_template('user/profil.html',activites=activites,liste=listes,id_pro=controle_pro, id_act=controle_act)




