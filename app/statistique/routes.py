import socket
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Historique, Organisation, Publication, Internaute, Historique
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RechercheForm
from . import stat
from ..utilites.utility import visiteur_annuelle, visiteurs_mensuele_rech, chiffre_sur_la_date, les_internautes, meilleur_article, visiteurs_mensuel, user_mac, les_visteurs_aujourd8, les_medias, les_publications, les_realisations, les_activites



@stat.route("/", methods=['GET','POST'])
@login_required
def index():
    form=RechercheForm()
    control_mois=None
    control_annee=None
    date_encours=None
    label=None
    data=None
    visite=None
    #Annee
    conrtrole_longeur_des_entree=[]
    if form.validate_on_submit():
        #Vérification du longeur des entrées
        if form.annee.data !='':
            conrtrole_longeur_des_entree.append(form.annee.data)
        if form.mois.data !='':
            conrtrole_longeur_des_entree.append(form.mois.data)

        #Verifification d'une seule entrée
        if len(conrtrole_longeur_des_entree)>1 or len(conrtrole_longeur_des_entree)==0:
            flash("Seulement une entrée est recommandée",'danger')
            return redirect(url_for('stat.index')) 
        #Affichage des messages
        if len(conrtrole_longeur_des_entree[0])>4:
            label, data, visite= visiteurs_mensuele_rech(conrtrole_longeur_des_entree[0])
            date_encours=conrtrole_longeur_des_entree[0]
            control_mois=True
        else:
            label, data, visite=visiteur_annuelle(conrtrole_longeur_des_entree[0])
            date_encours=conrtrole_longeur_des_entree[0]
            control_annee=True
            
            
            
    return render_template('statistique/cherche.html',control_annee=control_annee,control_mois=control_mois,date_encours=date_encours, form=form,label=label,data=data,visiteur=visite )


