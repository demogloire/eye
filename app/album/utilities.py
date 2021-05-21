import os
import secrets
from PIL import Image
from flask import redirect, session, url_for
from functools import wraps
from .. import create_app
from shutil import copyfile

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


def upload_acif(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'album' in session:
        return f(*args, **kwargs)
      else:
        return redirect(url_for('album.ajoutalbm'))
    return wrap

def upload_inactif(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'album' in session:
        session.pop('album', None)
        return f(*args, **kwargs)
      else:
        return f(*args, **kwargs)
    return wrap


def save_picture_thumb(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/publication', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_avatar_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/album', picture_fn)
    form_picture.save(picture_path)



def save_sup(fichier):
    if fichier is not None:
        chemin_offre=os.path.join(app.root_path, 'static/publication', fichier)
        if os.path.exists(chemin_offre):
            os.remove(chemin_offre)
        else:
            pass
    return True

def save_sup_av(fichier):
    if fichier is not None:
        chemin_offre=os.path.join(app.root_path, 'static/album', fichier)
        if os.path.exists(chemin_offre):
            os.remove(chemin_offre)
        else:
            pass
    return True



def copie_fichier(fichier):
  if fichier is not None:
    source=os.path.join(app.root_path, 'static/publication', fichier)
    destionation=os.path.join(app.root_path, 'static/album', fichier)
    #Copie du fichier de la destination
    copyfile(source, destionation)
    
  return fichier


