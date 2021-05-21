import os
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Media
from app.media.forms import AjoutMediaForm, EditMediaForm, EditVideoForm
#from app.evenement.upload import f_avatar
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, message_historique, find_url
#from slugify import slugify
from . import media
import timeago
from datetime import datetime
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url



''' Ajouter un media '''
@media.route('/ajouter', methods=['GET','POST'])
@login_required
def ajouter():
   title=title_page('Media')
   #formulaire
   form=AjoutMediaForm()

   if form.validate_on_submit():
      #Les variables de verifications des données
      ver_video=form.video.data
      ver_audio=form.audio.data
      enre_media=None
      message=None
      type_media=None
      url_video=None
      redirection=None
      
      print(ver_video,'dddddddddddddddddddddddddddddddddddddddddddd')

      if ver_video !=False or  find_url(form.url.data)==1 :
         if ver_video !=False:
            if find_url(form.url.data)==1:
               #Vérification de chaine de caractère
               if "watch?v=" in str(form.url.data):
                  url_video =str(form.url.data)
                  url_video = url_video.replace("watch?v=", "embed/")
                  enre_media=Media(titre=form.titre.data, type_media='Vidéo', url_media=url_video)
                  message=f"Enregistrement de l'url de la video {form.titre.data}"
                  type_media="Video"
               else:
                  enre_media=Media(titre=form.titre.data, type_media='Vidéo', url_media=form.url.data)
                  message=f"Enregistrement de l'url de la video {form.titre.data}"
                  type_media="Video"   
            else:
               flash("Le lien de la vidéo",'danger')
               return redirect(url_for('media.ajouter'))
         else:
            type_media="Audio"
            flash("Audio",'danger')
            return redirect(url_for('media.ajouter'))
                
      if ver_audio !=False or  form.mp_trois.data is not None:
         if ver_audio !=False:
            if form.mp_trois.data.filename !='':
               upload_result = upload(form.mp_trois.data, resource_type = "video")
               url_de_mp3=upload_result['url']
               enre_media=Media(titre=form.titre.data, type_media='Audio', url_media=url_de_mp3)
               message=f"Enregistrement de l'url de la video {form.titre.data}"
               type_media="Audio"
            else:
               flash("Charger la vidéo svp",'danger')
               return redirect(url_for('media.ajouter'))
         else:
            flash("Audio",'danger')
            return redirect(url_for('media.ajouter'))
      
      message_historique(message, user_ide=current_user.id)
      db.session.add(enre_media)
      db.session.commit()
      #Rédirection selon les médias
      if type_media=='Audio':
         return redirect(url_for('media.index_audio'))
      else:
         return redirect(url_for('media.index_video'))
         
   return render_template('media/ajouter.html',  title=title, form=form)


@media.route('/', methods=['GET', 'POST'])
@login_required
def index():

   #Titre
   title=title_page('Media')
   #Requête d'affichage des evenements
   listes=Media.query.order_by(Media.id.desc()).all()
   #Taille de evenements   
   taille=len(listes)

   return render_template('media/index.html',title=title, liste=listes, taille=taille)


#Rédirection selon le média audio
@media.route('/audio', methods=['GET', 'POST'])
@login_required
def index_audio():
   listes=Media.query.filter_by(type_media='Audio').order_by(Media.id.desc()).all()
   return render_template('media/index_audio.html', listes=listes)

#Rédirection selon le média video
@media.route('/video', methods=['GET', 'POST'])
@login_required
def index_video():
   listes=Media.query.filter_by(type_media='Vidéo').order_by(Media.id.desc()).all()
   return render_template('media/index_video.html', listes=listes)


@media.route('/edit_<int:media_id>', methods=['GET', 'POST'])
@login_required
def edit(media_id):
   #Modification
   form = EditMediaForm()
   #Titre
   title = title_page('Media')

   selec_media = Media.query.filter_by(id=media_id).first()
   
   if form.validate_on_submit():
       selec_media.titre=form.titre.data
       selec_media.type_media=form.type_media.data
       db.session.commit()
       #Enregistrement
       message=f"Modification du media :{form.titre.data}"
       message_historique(message)

       flash("Modification réussie",'primary')
       return redirect(url_for('media.index'))
      
   if request.method=='GET':
       form.titre.data=selec_media.titre
       form.type_media.data=selec_media.type_media
  

   return render_template('media/edit.html', form=form, title=title)

""" Modification statut """
@media.route('/statut/<int:media_id>', methods=['GET', 'POST'])
@login_required
def statut(media_id): 
   #Titre
   title=title_page('Media')
   #Requête de vérification du type
   selec_media=Media.query.filter_by(id=media_id).first_or_404()

   if selec_media is None:
      return redirect(url_for('media.index'))

   if selec_media.statut == True:
      selec_media.statut=False
      db.session.commit()
      flash("Ce media est désactivé sur la plateforme",'primary')
      return redirect(url_for('media.index'))
   else:
      selec_media.statut=True
      db.session.commit()
      flash("Ce media est activé sur la plateforme",'primary')
      return redirect(url_for('media.index'))   
   return render_template('media/index.html',title=title)



""" Suppression audio """
@media.route('/sup/<int:media_id>', methods=['GET', 'POST'])
@login_required
def sup_audio(media_id): 
   #Titre
   title=title_page('Media')
   #Requête de vérification du type
   selec_media=Media.query.filter_by(id=media_id).first_or_404()
   Media.query.filter_by(id=media_id).delete()
   db.session.commit()
   flash("L'audio est supprimée avec succès",'danger')
   return redirect(url_for('media.index_audio'))

""" Suppression vidéo """
@media.route('/sup/video/<int:media_id>', methods=['GET', 'POST'])
@login_required
def sup_video(media_id): 
   #Titre
   title=title_page('Media')
   #Requête de vérification du type
   selec_media=Media.query.filter_by(id=media_id).first_or_404()
   Media.query.filter_by(id=media_id).delete()
   db.session.commit()
   flash("La vidéo est supprimée avec succès",'danger')
   return redirect(url_for('media.index_video'))


@media.route('/audio/edit_<int:media_id>', methods=['GET', 'POST'])
@login_required
def edit_audio(media_id):
   #Modification
   form = EditMediaForm()
   #Titre
   title = title_page('Media')
   selec_media = Media.query.filter_by(id=media_id).first_or_404()
   if form.validate_on_submit():
       selec_media.titre=form.titre.data
       db.session.commit()
       #Enregistrement
       message=f"Modification du media :{form.titre.data}"
       message_historique(message, user_ide=current_user.id)
       flash("Modification réussie",'primary')
       return redirect(url_for('media.index_audio'))
   if request.method=='GET':
       form.titre.data=selec_media.titre
   return render_template('media/edit_audio.html', form=form, title=title)


@media.route('/video/edit_<int:media_id>', methods=['GET', 'POST'])
@login_required
def edit_video(media_id):
   #Modification
   form = EditVideoForm()
   #Titre
   title = title_page('Media')
   url_video=None
   
   selec_media = Media.query.filter_by(id=media_id).first_or_404()
   if form.validate_on_submit():
      if find_url(form.url.data)==1:
         if "watch?v=" in str(form.url.data):
            url_video =str(form.url.data)
            url_video = url_video.replace("watch?v=", "embed/")
         else:
            url_video=form.url.data
   
         selec_media.titre=form.titre.data
         selec_media.url_media=url_video
         db.session.commit()
         #Enregistrement
         message=f"Modification du media :{form.titre.data}"
         message_historique(message, user_ide=current_user.id)
         flash("Modification réussie",'primary')
         return redirect(url_for('media.index_video'))
   if request.method=='GET':
      form.titre.data=selec_media.titre
      form.url.data=selec_media.url_media
   return render_template('media/edit_video.html', form=form, title=title)


""" Modification statut """
@media.route('/audio/statut/<int:media_id>', methods=['GET', 'POST'])
@login_required
def statut_audio(media_id): 
   #Titre
   title=title_page('Media')
   #Requête de vérification du type
   selec_media=Media.query.filter_by(id=media_id).first_or_404()

   if selec_media is None:
      return redirect(url_for('media.index_audio'))

   if selec_media.statut == True:
      selec_media.statut=False
      db.session.commit()
      flash("Ce media est désactivé sur la plateforme",'primary')
      return redirect(url_for('media.index_audio'))
   else:
      selec_media.statut=True
      db.session.commit()
      flash("Ce media est activé sur la plateforme",'primary')
      return redirect(url_for('media.index_audio'))

   return render_template('media/index.html',title=title)



""" Modification statut """
@media.route('/video/statut/<int:media_id>', methods=['GET', 'POST'])
@login_required
def statut_video(media_id): 
   #Titre
   title=title_page('Media')
   #Requête de vérification du type
   selec_media=Media.query.filter_by(id=media_id).first_or_404()

   if selec_media is None:
      return redirect(url_for('media.index_video'))

   if selec_media.statut == True:
      selec_media.statut=False
      db.session.commit()
      flash("Ce media est désactivé sur la plateforme",'primary')
      return redirect(url_for('media.index_video'))
   else:
      selec_media.statut=True
      db.session.commit()
      flash("Ce media est activé sur la plateforme",'primary')
      return redirect(url_for('media.index_video'))

   return render_template('media/index.html',title=title)


""" Modifier à la une """
@media.route('/alaune/<int:med_id>', methods=['GET', 'POST'])
@login_required
def alune(med_id):
   #Titre
   title=title_page('Media')
   #Requête de vérification du type
   pub_c=Media.query.filter_by(id=med_id).first_or_404()
   
   if pub_c.type_media=='Audio':
      flash("Attention",'danger')
      return redirect(url_for('media.index_video'))
   
   #Vérification
   pub_all=Media.query.filter(Media.alaune==True, Media.id !=med_id).first()
   if pub_all is not None:
      pub_all.alaune=False
      db.session.commit()
   

   #Mise à jour de la predication à la une
   if pub_c.alaune == True:
      pub_c.alaune=False
      db.session.commit()
      flash("Le média n'est plus à la une",'success')
      return redirect(url_for('media.index_video'))
   else:
      pub_c.alaune=True
      db.session.commit()
      flash("Le média est à la une",'success')
      return redirect(url_for('media.index_video'))
   
   return render_template('user/index.html',title=title)



   