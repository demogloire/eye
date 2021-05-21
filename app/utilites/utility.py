from .. import db
from ..models import Historique, Internaute, Visiteur, Organisation, Media, Publication, Realisation, Categorie
from slugify import slugify
from datetime import datetime, date
from functools import wraps
import secrets
import random
import string
import time
import uuid
from flask import session, request
from getmac import get_mac_address
import re 
from flask_login import current_user
from flask import render_template, flash, url_for, redirect, request, session


#Titre
def title_page(nom="Dashbord"):
    title=f'{nom}'
    return title

#Historique
def message_historique(message=None, internaute=None, user=None, user_ide=None):
    historique=Historique(message=message, pseudonyme=user, user_id=user_ide, internaute_id=internaute)
    db.session.add(historique)
    db.session.commit()

#Slug de l'article
def slug_publication(titre=None):
    return slugify(titre)


#Utilisateur unique
def code_usermac(length=4):
    #Code pour généer un mot de passe unique
    your_letters='AEIOU1234567890'
    return ''.join((random.choice(your_letters) for i in range(length)))


def random_avatar():
    chiffre=random.randint(1, 5)
    avatar=None
    if chiffre == 1:
        avatar='1.png'
    elif chiffre == 2:
        avatar='2.png'
    elif chiffre == 3:
        avatar='3.png'
    elif chiffre == 4:
        avatar='4.png'
    else:
        avatar='5.png'
    return avatar
        
    

#Les nombres de visteurs par jours
def lesvisteurs():
    if 'visiteur' in session:
        pass
    else:
        session["visiteur"]=True
        date_aujour=date.today()
        dt_ver=Visiteur.query.filter_by(date_vist=date_aujour).first()
        if dt_ver is None:
            compteur=Visiteur(nombre_vis=1, date_vist=date_aujour)
            db.session.add(compteur)
            db.session.commit()
        else:
            dt_ver.nombre_vis=dt_ver.nombre_vis+1
            db.session.commit()


#Adresse mac unique
def macadress():
    var=':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return var

#Mac cart de session
def adresse_mac_carte():
    request_v=get_mac_address(ip='{}'.format(request.remote_addr), network_request=True)
    return request_v



#Ideintification de l'utilisateur sur base de l'adresse MAC
def user_mac():
    code_user=None
    adre_unique_mac=None
    if request.remote_addr=='127.0.0.1':
        adre_unique_mac=macadress()
        code_user=code_usermac()
    else:
        adre_unique_mac=adresse_mac_carte()
        code_user=code_usermac()
        
    verification_internaute=Internaute.query.filter_by(adress_mac=adre_unique_mac).first()
    if verification_internaute is None:
        visiteur_user=Internaute(pseudonyme=code_user, adress_mac=adre_unique_mac, avatar=random_avatar())
        db.session.add(visiteur_user)
        db.session.commit()
        return visiteur_user.id
    else:
        return verification_internaute.id


#Enregistremt de l'article lu en cours
def enr_art(article, var_lu_art, article_pu):
    if article is False and var_lu_art==False:
      article_nombre_lu=article_pu.nbr_lu+1
      article_pu.nbr_lu=article_nombre_lu
      db.session.commit()
      session["ver"]=article_pu.id
    elif article is True and var_lu_art==False or article is False and var_lu_art==True :
        article_nombre_lu=article_pu.nbr_lu+1
        article_pu.nbr_lu=article_nombre_lu
        db.session.commit()
        session["ver"]=article_pu.id



#verification de l'article
def ver_enre_article(id_art):
    variable=False
    if 'id_pu' in session:
        id_pub = session['id_pu']
        if id_art==id_pub:
            variable=True
        else:
            variable=id_pub
    else:
        variable=False
    return variable

#verification de l'article pour marque comme lues
def ver_enre_lu(id_art):
    variable=False
    if 'ver' in session:
        id_pub = session['ver']
        if id_art==id_pub:
            variable=True
        else:
            variable=False
    else:
        variable=False
    return variable

    #Enregistrement et modification d'une photo
def split_string(data):
    data_split=data.split('/')
    return data_split

def date_sup_ver(premier, deuxieme):
    date_string_un=str(premier)
    date_string_deux=str(deuxieme)
    date_un_split=split_string(date_string_un)
    date_deux_split=split_string(date_string_deux)

    ver_date_une=datetime(int(date_un_split[2]), int(date_un_split[1]), int(date_un_split[0]))
    ver_date_deux=datetime(int(date_deux_split[2]), int(date_deux_split[1]), int(date_deux_split[0]))
    return ver_date_deux <= ver_date_une

def split_string_data(data):
    data_split=data.split('/')
    date='{}-{}-{}'.format(data_split[2], data_split[1], data_split[0])
    return date

#Date de la modification
def date_modification():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string

def split_string_data_form(data):
    data=str(data)
    data_split=data.split('-')
    date='{}/{}/{}'.format(data_split[2], data_split[1], data_split[0])
    return date

  
def find_url(string): 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    liste_url=[x[0] for x in url]
    return len(liste_url) 

def organisation():
    org=Organisation.query.first()
    return None

#Les statistiques
def les_visteurs_aujourd8():
    nombre=0
    aujourd8=str(date.today())
    visiteur=Visiteur.query.filter_by(date_vist=aujourd8).first()
    if visiteur is None:
        nombre=nombre
    else:
        nombre=visiteur.nombre_vis
    return nombre

def les_medias():
    nombre=[]
    media=Media.query.filter_by(statut=True).all()
    if media is None:
        nombre.append(0)
    else:
        for i in media:
            nombre.append(i.id)
    return len(nombre)


def les_publications():
    nombre=[]
    publ=Publication.query.filter_by(statut=True).all()
    if publ is None:
        nombre.append(0)
    else:
        for i in publ:
            nombre.append(i.id)
    return len(nombre)


def les_realisations():
    nombre=[]
    real=Realisation.query.filter_by(statut=True).all()
    if real is None:
        nombre.append(0)
    else:
        for i in real:
            nombre.append(i.id)
    return len(nombre)

def les_activites():
    nombre=[]
    act=Historique.query.filter_by(user_id=current_user.id).all()
    if act is None:
        nombre.append(0)
    else:
        for i in act:
            nombre.append(i.id)
    return len(nombre)


def visiteurs_mensuel():
    mois=[]
    chiffre=[]
    date_en=f'{date.today()}'
    date_format_avant=str(date_en).split("-")
    date_annee="%{}-{}%".format(date_format_avant[0],date_format_avant[1])
    visiteur=Visiteur.query.filter(Visiteur.date_vist.ilike(date_annee)).order_by(Visiteur.id.asc()).all()
    for i in visiteur:
        date_encours=str(i.date_vist).split("-")
        mois.append("{}".format(date_encours[2]))
        chiffre.append(i.nombre_vis)
    return mois,chiffre
        

def meilleur_article():
    article_utilisateur=[]
    titre_meilleur_pub=[]
    score_de_meilleur=[]
    score_art_1=None
    score_art_2=None
    score_totale=Publication.query.all()
    score_article=Publication.query.filter(Publication.nbr_lu >=5).limit(2)
    for i in score_totale:
        article_utilisateur.append(i.nbr_lu)
    for i in score_article:
        titre_meilleur_pub.append(i.titre)
        score_de_meilleur.append(i.nbr_lu)
    if len(titre_meilleur_pub) > 1:
        val_1=round((int(score_de_meilleur[0])/int(sum(article_utilisateur)))*100,2)
        val_2=round((int(score_de_meilleur[1])/int(sum(article_utilisateur)))*100,2)
        score_art_1=[titre_meilleur_pub[0],val_1]
        score_art_2=[titre_meilleur_pub[1],val_2]
    else:
        return None
        
    return score_art_1, score_art_2

def les_internautes():
    inter=Historique.query.filter(Historique.internaute_id !=None).order_by(Historique.id.desc()).limit(100)
    return inter
        

def chiffre_sur_la_date(annee=None, redirection=None):
    annee_convert=None
    if annee_convert!=4:
        flash("Date à 4 chiffre seuelement",'danger')
        return redirect(url_for('{}'.format(redirection)))    
    else:
        try:
            annee_convert=int(str(form.annee.data))
        except:
            flash("Date à 4 chiffre seuelement",'danger')
            return redirect(url_for('{}'.format(redirection))) 
    return annee_convert
        

def personalisation_mois(data):
    mois=None
    if data=='01':
        mois="Jan"
    elif data=='02':
        mois="Fév"
    elif data=='03':
        mois="Mar"
    elif data=='04':
        mois="Avr"
    elif data=='05':
        mois="Mai"
    elif data=='06':
        mois="Juin"
    elif data=='07':
        mois="Juil"
    elif data=='08':
        mois="Aoû"
    elif data=='09':
        mois="Sép."
    elif data=='10':
        mois="Oct"
    elif data=='11':
        mois="Nov"
    elif data=='12':
        mois="Déc"
    return mois
    
        


def visiteurs_mensuele_rech(data):
    mois=[]
    chiffre=[]
    date_en=f'{data}'
    date_format_avant=str(date_en).split("/")
    date_annee="%{}-{}%".format(date_format_avant[1],date_format_avant[0])
    visiteur=Visiteur.query.filter(Visiteur.date_vist.ilike(date_annee)).order_by(Visiteur.id.asc()).all()
    for i in visiteur:
        date_encours=str(i.date_vist).split("-")
        mois.append("{}/{}".format(date_encours[2],date_encours[1]))
        chiffre.append(i.nombre_vis)
    return mois,chiffre, visiteur


def visiteur_annuelle(data):
    vis_an_c={}
    mois=[]
    chiffre=[]
    dictlist=[]
    date_annee="%{}%".format(data)
    visit_par_mois=Visiteur.query.filter(Visiteur.date_vist.ilike(date_annee)).order_by(Visiteur.id.asc()).all()
    
    for i in visit_par_mois:
        date_format_avant=str(i.date_vist).split("-")
        date_encours_par_mois=f"{personalisation_mois(date_format_avant[1])}-{date_format_avant[0]}"
        if date_encours_par_mois in vis_an_c:
            pass
        else:
            vis_an_c[date_encours_par_mois]=int(i.nombre_vis)
            
    for i in visit_par_mois:
        date_format_avant=str(i.date_vist).split("-")
        date_encours_par_mois=f"{personalisation_mois(date_format_avant[1])}-{date_format_avant[0]}"
        if date_encours_par_mois in vis_an_c:
            vis_an_c[date_encours_par_mois]=int(vis_an_c[date_encours_par_mois])+int(i.nombre_vis)
    #Les informations du dictionnaire
    for i,v in vis_an_c.items():
        mois.append(i)
        chiffre.append(v)
    
    #Convertion du dictionnaire en liste
    for key, value in vis_an_c.items():
        temp = [key,value]
        dictlist.append(temp)
    
    return mois,chiffre, dictlist


#Autorisation des collaborateurs
def webmaster_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role =='Administrateur' or current_user.role=='Webmaster':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.dashboard'))       
    return wrap

def admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role =='Administrateur':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.dashboard'))       
    return wrap
    

def recent_artcile():
    categorie=Categorie.query.filter_by(nom="Actualités").first()
    recent_a=None
    if categorie is not None:
        recent_a=Publication.query.filter_by(categorie_id=categorie.id).order_by(Publication.id.desc()).limit(3).all()
    else:
        recent_a=[]
    return recent_a
    
        
    
    
    
        
            
        
    
        
        
    
    

    
    