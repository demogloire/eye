import socket
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Historique, Organisation, Publication, Internaute, Historique, Donation
from flask_login import login_user, current_user, logout_user, login_required
from . import main
from ..utilites.utility import les_internautes, meilleur_article, visiteurs_mensuel, user_mac, les_visteurs_aujourd8, les_medias, les_publications, les_realisations, les_activites



@main.route("/")
@login_required
def dashboard():
    label, data=visiteurs_mensuel()
    activites=Historique.query.order_by(Historique.id.desc()).limit(4)
    activite=Historique.query.filter_by(user_id=current_user.id).order_by(Historique.id.desc()).limit(4)
    #Les meilleurs lectures
    un=None
    deux=None
    controle=None
    if meilleur_article() is None:
        controle=None
    else:
        un,deux=meilleur_article()
        controle=True
    
    
    return render_template('main/index.html',title="Dashboard",internaute=les_internautes(), controle=controle, un=un,deux=deux, label=label, data=data, visteur=les_visteurs_aujourd8(),media=les_medias(), publication=les_publications(),
                           realisation=les_realisations(), activites=les_activites(), act_user=activite, activite=activites)


@main.route("/recette")
@login_required
def recette():
    don=Donation.query.order_by(Donation.id.desc()).all()
    
    return render_template('main/don.html',title="Recette", don=don)



