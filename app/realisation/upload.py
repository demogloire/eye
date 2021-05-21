import os
import secrets
from PIL import Image
from .. import create_app




config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)



#Enregistrement du fichier pdf
def publication_doc(document):
    if document is None:
        return None
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(document.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/publication', picture_fn)
    document.save(picture_path)
    return picture_fn

#Enregistrement du fichier 
def save_image_mod(form_picture, ancien):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #Suppression de l'ancien fichier
    if ancien is not None:
        chemin_offre=os.path.join(app.root_path, 'static/publication', ancien)
        if os.path.exists(chemin_offre):
            os.remove(chemin_offre)
        else:
            pass
    #Enregitrement du nouveau fichier
    picture_path = os.path.join(app.root_path, 'static/publication', picture_fn)
    form_picture.save(picture_path)
    return picture_fn



def f_avatar(form_picture):
    random_hex= secrets.token_hex(8)
    _, f_ext= os.path.splitext(form_picture.filename)
    picture_fn= random_hex + f_ext
    picture_path= os.path.join(app.root_path, 'static/image', picture_fn)
    print(picture_path,'**********************************************************')
    output_sz= (800, 500)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)
    return picture_fn

