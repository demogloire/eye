from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Album, Galerie, Historique
from app.album.forms import AjoutPhoForm, AjoutEdPForm, AjoutCatForm, EditCatForm
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, slug_publication, message_historique, date_modification, organisation

from . import album

from app.album.utilities import upload_acif, upload_inactif,save_sup_av, save_picture_thumb, save_sup,copie_fichier, save_avatar_image



''' Ajoute d'un album '''
@album.route('/ajou_album', methods=['GET', 'POST'])
@login_required
@upload_inactif
def ajoutalbm():
   #Titre 
   title="Création d'album"
   #formulaire
   form=AjoutCatForm()

   if form.validate_on_submit():
      nom_cat=form.nom.data.capitalize()
      album_enre=Album(noms=nom_cat)
      db.session.add(album_enre)
      db.session.commit()
      session['album'] = album_enre.id
      session['nom_album']=album_enre.noms
      message=f"Ajout de l'album:{nom_cat}"
      message_historique(message=message,user_ide=current_user.id)
      return redirect(url_for('album.mediaalbm')) 
   return render_template('album/ajouter.html',  title=title, form=form, organisation=organisation())


@album.route('/media_ajout', methods=['GET', 'POST'])
@login_required
@upload_acif
def mediaalbm():

   #Titre 
   title="Média"
   #formulaire
   form=AjoutPhoForm()

     #Les information de l'album encours d'enregistrements
   if 'album' in session and 'nom_album' in session:
      id_album=session['album']
      nom_album=session['nom_album']

   album_picture=Album.query.filter_by(id=id_album).first_or_404()

   if form.validate_on_submit():
      if form.file.data:
         img_photo=save_picture_thumb(form.file.data)
         enre_media=Galerie(url=img_photo, album_id=id_album)
         if album_picture.nbr_picture==0:
            album_picture.avatar=copie_fichier(img_photo)
         album_picture.nbr_picture=int(album_picture.nbr_picture)+1
         db.session.add(enre_media)
         db.session.commit()
         message=f"Ajout de l'image :{img_photo}"
         message_historique(message=message,user_ide=current_user.id)
         flash("Ajout dans l'album avec succès", "success")
         return redirect(url_for('album.mediaalbm')) 
         
   return render_template('album/ulpload_img.html',nom_album=nom_album, organisation=organisation(),  title=title, id_a=id_album, form=form, album=album_picture.galeries)


""" Liste des albums"""
@album.route('/', methods=['GET', 'POST'])
@login_required
def index():
   #Titre
   title='Liste des albums'
   #Requête d'affichage de la categorisation
   listes=Album.query.order_by(Album.id.desc()).all()
   return render_template('album/views.html',title=title,organisation=organisation(), liste=listes)



"""Activation d'album """

@album.route('/statut_album/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def statutalb(cat_id):
   #Titre
   title="L'album"


   #Requête de vérification de l'album
   cat_statu=Album.query.filter_by(id=cat_id).first_or_404()

   if cat_statu is None:
      return redirect(url_for('album.index')) 

   if cat_statu.statut == True:
      cat_statu.statut=False
      db.session.commit()
      message=f"Désactivation du statut en de l'abum {cat_statu.noms}"
      message_historique(message=message,user_ide=current_user.id)
      flash("L'album est désactivé sur la plateforme",'success')
      return redirect(url_for('album.index')) 
   else:
      cat_statu.statut=True
      db.session.commit()
      message=f"Activation du statut en de l'abum {cat_statu.noms}"
      message_historique(message=message,user_ide=current_user.id)
      flash("L'album est activée sur la plateforme",'success')
      return redirect(url_for('album.index'))
   
   
   return render_template('user/views.html',title=title,organisation=organisation())

@album.route('finupload', methods=['GET', 'POST'])
def terminerupload():

   if 'album' in session:
      session.pop('album', None)
      return redirect(url_for('album.index'))
   else:
      return redirect(url_for('album.index'))
          



# """ Modification de la catégorie  """

@album.route('/edit_<int:cate_id>_cate', methods=['GET', 'POST'])
@login_required
def editalbum(cate_id):
          
   form=EditCatForm()
   #Titre
   title="Modification de l'album"
   #Requête de vérification de l'album
   cate_class=Album.query.filter_by(id=cate_id).first()
   #Le nom du type encours de modification
   cate_nom=cate_class.noms

   if cate_class is None:
      return redirect(url_for('album.index'))
   
   if form.validate_on_submit(): 
      cate_class.noms=form.ed_nom.data.capitalize()
      db.session.commit()
      message=f"Modification de l'abum {cate_class.noms}"
      message_historique(message=message,user_ide=current_user.id)
      flash("Modification réussie",'success')
      return redirect(url_for('album.index'))
      
   if request.method=='GET':
      form.ed_nom.data=cate_class.noms
      
   return render_template('album/edit.html', form=form, title=title, cate_nom=cate_nom, organisation=organisation())


@album.route('/media_ajout/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def mediaaled(cate_id):
    #Titre 
   title="Média"
   #formulaire
   form=AjoutEdPForm()

   upload_result=None

   cate_class=Album.query.filter_by(id=cate_id).first_or_404()
   #De nom de l'album
   nom_album=cate_class.noms
   #Le nom du type encours de modification
   if cate_class is None:
      return redirect(url_for('album.index'))
   
   if form.validate_on_submit():
      if form.file.data:
         img_file=save_picture_thumb(form.file.data)
         enre_media=Galerie(url=img_file, album_id=cate_id)
         cate_class.nbr_picture= int(cate_class.nbr_picture) + 1
         db.session.add(enre_media)
         db.session.commit()
         message=f"Ajout de l'image dans l'album {cate_class.noms}"
         message_historique(message=message,user_ide=current_user.id)
         flash("Vous avez ajouté une image dans votre album", "success")
         return redirect(url_for('album.mediaaled', cate_id=cate_id)) 
         
   return render_template('album/ulpload_imgc.html',nom_album=nom_album,id_a=cate_id, album=cate_class.galeries,  title=title, form=form, organisation=organisation())


@album.route('/<int:cat_id>/sup_<int:photo_id>', methods=['GET', 'POST'])
@login_required
def sup_photo(cat_id, photo_id): 
   #Notifcation
   
   #Requête de vérification de l'image dans l'album
   sup_image=Galerie.query.filter_by(id=photo_id).first_or_404()
   cate_class=Album.query.filter_by(id=cat_id).first()
   #Message historique
   message=f"Suppression de l'image ({sup_image.url}) de l'abum {cate_class.noms}"
   message_historique(message=message,user_ide=current_user.id)
   #Supression de l'image
   save_sup(sup_image.url)
   Galerie.query.filter_by(id=photo_id).delete()
   cate_class.nbr_picture= int(cate_class.nbr_picture) - 1
   db.session.commit()
   
   flash("Suppression réussie",'danger')
   return redirect(url_for('album.mediaalbm'))



@album.route('/sup/<int:cat_id>/sup_<int:photo_id>', methods=['GET', 'POST'])
@login_required
def sup_photo_add(cat_id, photo_id): 
   #Requête de vérification de l'image dans l'album
   sup_image=Galerie.query.filter_by(id=photo_id).first_or_404()
   cate_class=Album.query.filter_by(id=cat_id).first()
   #Message historique
   message=f"Suppression de l'image ({sup_image.url}) de l'abum {cate_class.noms}"
   message_historique(message=message,user_ide=current_user.id)
   #Supression de l'image
   save_sup(sup_image.url)
   Galerie.query.filter_by(id=photo_id).delete()
   cate_class.nbr_picture= int(cate_class.nbr_picture) - 1
   db.session.commit()
   flash("Suppression réussie",'danger')
   return redirect(url_for('album.mediaaled', cate_id=cat_id ))


@album.route('/sup/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def sup_album(cat_id): 
   liste_d_image=[]
   #Requête de vérification de l'image dans l'album
   cate_class=Album.query.filter_by(id=cat_id).first_or_404()
   message=f"Suppression de l'abum {cate_class.noms}"
   message_historique(message=message,user_ide=current_user.id)
   
   for i in cate_class.galeries:
      Galerie.query.filter_by(id=i.id).delete()
      liste_d_image.append(str(i.url))
      save_sup(i.url)
      db.session.commit()
   save_sup_av(cate_class.avatar)
   Album.query.filter_by(id=cat_id).delete()
   db.session.commit()
   flash("Album supprimer",'danger')
   return redirect(url_for('album.index'))





