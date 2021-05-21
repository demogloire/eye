from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User, Publication, Categorie, Historique, Commentaire, Comment, Galerie, Album, Fichier, Evenement, Media
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date
import flask_sijax
from ..utilites.utility import webmaster_admin, recent_artcile, les_visteurs_aujourd8, ver_enre_article, ver_enre_lu, enr_art, lesvisteurs, title_page, slug_publication, message_historique, date_modification,user_mac
from . import cbca
import timeago
from .forms import FormCommetaire, FormCommetaired



#Time ago
@cbca.context_processor
def utility_processor():
    def timeagos(date_time):
        date_maintenant = datetime.now()
        date_encours=timeago.format(date_time, date_maintenant, 'fr')
        return date_encours
    return dict(timeagos=timeagos)

@cbca.context_processor
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


@cbca.context_processor
def utility_processor():
    def date_french(date_sp):
        mois_anglais=date_sp.strftime('%B')
        mois_francais=None
        jour_francais=date_sp.strftime('%d')
        annee_francais=date_sp.strftime('%Y')
        #Les jours en anglais
        if mois_anglais=='January':
            mois_francais="Janvier"
        elif mois_anglais=="February":
            mois_francais="Février"
        elif mois_anglais=="March":
            mois_francais="Mars"
        elif mois_anglais=="April":
            mois_francais="Avril"
        elif mois_anglais=="May":
            mois_francais="Mai"
        elif mois_anglais=="June":
            mois_francais="Juin"
        elif mois_anglais=="July":
            mois_francais="Juillet"
        elif mois_anglais=="August":
            mois_francais="Août"
        elif mois_anglais=="September":
            mois_francais="Septembre"
        elif mois_anglais=="October":
            mois_francais="Octobre"
        elif mois_anglais=="November":
            mois_francais="Novembre"
        elif mois_anglais=="December":
            mois_francais="Décembre"
        #Date formatage complete
        date_complete=f"{jour_francais} {mois_francais} {annee_francais}"
        return date_complete
    return dict(date_french=date_french)



""" Acceuil """
@cbca.route("/")
def accueil():
    #Titre de l'onglet
    title=title_page('Accueil')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    fichier=None
    #Liste des actualités sur la plateforme
    message=f"Visite de l'acceuil"
    message_historique(message=message, internaute=mac_utilisateur)
    cate_id=Categorie.query.filter_by(nom="Actualités").first()
    #Publication
    pub=Publication.query.filter_by(statut=True, categorie_id=cate_id.id).order_by(Publication.id.asc()).limit(3).all()
    #Photo
    photo=Galerie.query.filter(Album.statut==True).order_by(Galerie.id.asc()).limit(4).all() #Les photos
    #Photo à une
    ala_une=Publication.query.filter(Publication.statut==True,Publication.pred_jour==True, Categorie.nom=='Prédications').first()
    #Evenement de l'Eglise
    date_actuelle=datetime.utcnow()
    evenements=Evenement.query.filter(date_actuelle <= Evenement.date_fin , Evenement.statut==True).order_by(Evenement.date_even.desc()).limit(3).all()
    #Requête des audio
    video_alaune=Media.query.filter_by(alaune=True, statut=True).first()
    #Video à la une
    media_predication=Media.query.order_by(Media.id.desc()).limit(3).all()

    #Ala une  
    if ala_une is not None:
        fichier_doc=Fichier.query.filter_by(publication_id=ala_une.id).first()
        if fichier_doc is not None:
            fichier=fichier_doc.url_pdf
    return render_template('cbca/index.html',media_predication=media_predication,video_alaune=video_alaune, evenements=evenements, title=title, pub=pub, photos=photo, ala_une=ala_une,fichier=fichier)


# @coedac.route('/apropos')
# def apropos():
#     #Titre de l'onglet
#     title=title_page('Apropos de nous')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     message=f"Visite de l'apropos de nous"
#     message_historique(message=message, internaute=mac_utilisateur)

#     page="Qui sommes-nous"
    
#     return render_template('coadec/about.html',title=title, page=page)

# @coedac.route('/predications')
# def predication():
#     #Titre de l'onglet
#     title=title_page('Prédication')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     page="Prédication"
#     #Prédication
#     message=f"Visite de la prediction"
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Liste des prédications
#     page= request.args.get('page', 1, type=int)
#     cate_id=Categorie.query.filter_by(nom="Predications").first()
#     predication=Publication.query.filter(Publication.statut==True,Publication.categorie_id==cate_id.id).order_by(Publication.id.desc()).paginate(page=page, per_page=6)
  
#     return render_template('coadec/predication.html',title=title, page=page, predication=predication)


# """ Prédication """
# @coedac.route('/predication/<string:slug>')
# def predication_une(slug):
#     #Vérification de la prédication
#     article_pu=Publication.query.filter_by(slug=slug).first_or_404()
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
    
#     if article_pu is not None:
#         session["id_pu"] = article_pu.id

#     #Publication des recentes publications sur la plateforme
#     post_recent=recent_artcile()
#     #Message d'alerte
#     message=f"Visite de la predication:{article_pu.titre} "
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Nombre des lis de l'article
#     article=ver_enre_article(article_pu.id)
#     var_lu_art=ver_enre_lu(article_pu.id)
#     enr_art(article,var_lu_art,article_pu)
#     #Formulaire
#     pub_meilleur=Publication.query.filter(Publication.nbr_lu > 10 , Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.nbr_lu.desc()).limit(6).all()
#     #Fichier encours d'éxecution
#     fichier_docu=Fichier.query.filter_by(publication_id=article_pu.id).first()
#     return render_template('coadec/une_pred.html',title="Actualité", page="Actualité", post_recent=post_recent,  pub_meilleur=pub_meilleur, une_pub=article_pu, fichier=fichier_docu)


# @coedac.route('/evenements')
# def evenement():
#     #Titre de l'onglet
#     title=title_page('Evénement')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     #Message d'alerte
#     message=f"Visite de l'événement "
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Liste les évenements
#     page= request.args.get('page', 1, type=int)
#     evenement=Evenement.query.filter_by(statut=True).order_by(Evenement.date_fin.desc()).paginate(page=page, per_page=6)
#     #Publication des recentes publications sur la plateforme
#     post_recent=recent_artcile()
#     return render_template('coadec/evenement.html', post_recent=post_recent, title=title, evenement=evenement)


# @coedac.route('/medias')
# def medias():
#     #Titre de l'onglet
#     title=title_page('Apropos de nous')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     message=f"Visite des audios"
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Les methodes des video
#     page= request.args.get('page', 1, type=int)
#     audio=Media.query.filter_by(type_media="Audio", statut=True).paginate(page=page, per_page=12)
#     #Publication des recentes publications sur la plateforme
#     post_recent=recent_artcile()
#     return render_template('coadec/media.html',title=title,audio=audio, post_recent=post_recent )


# @coedac.route('/video/medias')
# def media_video():
#     #Titre de l'onglet
#     title=title_page('Apropos de nous')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     message=f"Visite des vidéo"
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Les methodes des video
#     page= request.args.get('page', 1, type=int)
#     audio=Media.query.filter_by(type_media="Vidéo", statut=True).paginate(page=page, per_page=12)
#     #La liste à transfert
#     liste_transfert=[]
#     for i in audio.items:
#         url_formetter=i.url_media.replace("https://www.youtube.com/embed/", "")
#         liste_transfert.append(url_formetter)
#     #Publication des recentes publications sur la plateforme
#     post_recent=recent_artcile()
#     return render_template('coadec/media_video.html',title=title,audio=audio, post_recent=post_recent, liste_transfert=liste_transfert )


# @coedac.route('/galerie')
# def galerie():
#     #Titre de l'onglet
#     title=title_page("Gélerie")
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     page="Galerie"
#     message=f"Visite de la galérie"
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Album actif
#     photo_al_actif=None
#     album_actif=Album.query.filter_by(statut=True).order_by(Album.id.asc()).first()
#     if album_actif is not None:
#         photo_al_actif=Galerie.query.filter_by(album_id=album_actif.id).all() 

#     album=Album.query.filter(Album.statut==True, Album.id != album_actif.id ).order_by(Album.id.desc()).all()
#     #Les articles de recentes
#     post_recent=recent_artcile()
    
#     return render_template('coadec/galerie.html',title=title, post_recent=post_recent, page=page, album=album, album_actif=album_actif, photo_al_actif=photo_al_actif)


# @coedac.route('/<int:id>/galerie')
# def galerie_trie(id):
#     #Titre de l'onglet
#     title=title_page("Galerie")
#     #album encours
#     nom_al=Album.query.filter_by(id=id).first_or_404()
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#    #Album actif
#     photo_al_actif=None
#     message=f"Visite de l'album: {nom_al.noms} "
#     message_historique(message=message, internaute=mac_utilisateur)
#     album_actif=Album.query.filter_by(id=id).order_by(Album.id.asc()).first()
#     if album_actif is not None:
#         photo_al_actif=Galerie.query.filter_by(album_id=album_actif.id).all() 

#     album=Album.query.filter(Album.statut==True, Album.id != album_actif.id ).order_by(Album.id.desc()).all()
#     #Les articles de recentes
#     post_recent=recent_artcile()
    
#     return render_template('coadec/galerie_trie.html',title=title, post_recent=post_recent,  album=album, album_actif=album_actif, photo_al_actif=photo_al_actif)


# @coedac.route('/actus')
# def actualites():
#     #Titre de l'onglet
#     title=title_page('Prédication')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     page="Prédication"
#     #Prédication
#     message=f"Visite des actualités"
#     message_historique(message=message, internaute=mac_utilisateur)
#     #Liste des actualités
#     page= request.args.get('page', 1, type=int)
#     cate_id=Categorie.query.filter_by(nom="Actualités").first()
#     actualites=Publication.query.filter(Publication.statut==True,Publication.categorie_id==cate_id.id).order_by(Publication.id.desc()).paginate(page=page, per_page=6)
#     return render_template('coadec/actualites.html',title=title, page=page, actualites=actualites)


# # """ Article """
# @coedac.route('/article/<string:slug>')
# def article(slug):
#     #Article de verification.
#     article_pu=Publication.query.filter_by(slug=slug).first_or_404()
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
        
#     if article_pu is not None:
#         session["id_pu"] = article_pu.id

#     #Nombre des lis de l'article
#     article=ver_enre_article(article_pu.id)
#     var_lu_art=ver_enre_lu(article_pu.id)
#     enr_art(article,var_lu_art,article_pu)
    
#     message=f"Visite de l'actualité :{article_pu.titre} "
#     message_historique(message=message, internaute=mac_utilisateur)

#     post_recent=Publication.query.filter(Publication.nbr_lu > 10 , Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.nbr_lu.desc()).limit(6).all()
#     album=Album.query.filter_by(statut=True).order_by(Album.id.asc()).all()
#     #Fichier encours d'éxecution
#     fichier_docu=Fichier.query.filter_by(publication_id=article_pu.id).first()
    
#     return render_template('coadec/actua_une.html', post_recent=post_recent, article_pu=article_pu,  album=album, fichier_docu=fichier_docu)


# @coedac.route('/contact')
# def contact():
#     #Titre de l'onglet
#     title=title_page('Contact')
#     #Visteur en ligne
#     lesvisteurs()
#     # L'utilisateur en cours
#     mac_utilisateur=user_mac()
#     message=f"Visite des contact"
#     message_historique(message=message, internaute=mac_utilisateur)


    
#     return render_template('coadec/contact.html',title=title)
