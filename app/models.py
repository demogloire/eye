from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    publications = db.relationship('Publication', backref='cat_pub', lazy='dynamic')
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    statut = db.Column(db.Boolean, default=False)  
    def __repr__(self):
        return ' {} '.format(self.nom)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    resume = db.Column(db.Text)
    slug=db.Column(db.String(255))
    statut = db.Column(db.Boolean, default=False)
    url_img= db.Column(db.String(128))
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nbr_lu=db.Column(db.Integer, default=0)
    nbr_like=db.Column(db.Integer, default=0)
    nbr_cmt=db.Column(db.Integer, default=0)
    url_youtube=db.Column(db.String(255))
    pred_jour=db.Column(db.Boolean, default=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    fichiers = db.relationship('Fichier', backref='pub_fic', lazy='dynamic')
    commentaires = db.relationship('Commentaire', backref='pub_com', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.titre)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    post_nom = db.Column(db.String(128))
    prenom= db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    role = db.Column(db.String(128))
    password_onhash = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar=db.Column(db.String(128), default='user.png')
    publications = db.relationship('Publication', backref='user_pub', lazy='dynamic')
    historiques = db.relationship('Historique', backref='user_his', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)



class Autorisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50))
    role=db.Column(db.String(50))
    statut = db.Column(db.Boolean, default=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return ' {} '.format(self.nom)

class Internaute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adress_mac = db.Column(db.String(200))
    pseudonyme = db.Column(db.String(200))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar=db.Column(db.String(200), default='1.png')
    historiques = db.relationship('Historique', backref='inter_hist', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nombre_v_par)


class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False) 
    primaire = db.Column(db.Boolean, default=False) 
    secondaire = db.Column(db.Boolean, default=False) 
    id_primaire = db.Column(db.Integer) 
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False) 
    comments = db.relationship('Comment', backref='comment_com', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.commentaire)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False) 
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaire.id'), nullable=False) 
    def __repr__(self):
        return ' {} '.format(self.commentaire)
    

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noms = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128), default='album.jpg')
    nbr_picture=db.Column(db.Integer, default=0)
    galeries = db.relationship('Galerie', backref='galerie_album', lazy='dynamic')
    statut= db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Album('{self.noms}')"

class Galerie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    url = db.Column(db.String(128))
    
    def __repr__(self):
        return f"Galerie('{self.url}')"


class Evenement (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    lieu = db.Column(db.String(200))
    message = db.Column(db.Text)
    avatar=db.Column(db.String(128))
    date_even=db.Column(db.Date, nullable=False, default=datetime.utcnow)
    date_fin=db.Column(db.Date, nullable=False, default=datetime.utcnow)
    statut=db.Column(db.Boolean, default=False)
    fichiers = db.relationship('Fichier', backref='evenement_fichier', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.message)

class Realisation (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    message = db.Column(db.Text)
    avatar=db.Column(db.String(128))
    date_realisation=db.Column(db.Date, nullable=False)
    image_article =db.Column(db.String(128))
    pdf_document = db.Column(db.String(128))
    lieu=db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)
    fichiers = db.relationship('Fichier', backref='realisation_fic', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.message)


class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    pseudonyme = db.Column(db.String(128))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    internaute_id = db.Column(db.Integer, db.ForeignKey('internaute.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    def __repr__(self):
        return ' {} '.format(self.message)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre=db.Column(db.String(128))
    type_media = db.Column(db.String(128))
    url_media =db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)
    alaune=db.Column(db.Boolean, default=False)
    fichiers = db.relationship('Fichier', backref='media_fic', lazy='dynamic')
    date_add=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Media('{self.titre}')"

class Fichier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_img= db.Column(db.String(128))
    url_pdf= db.Column(db.String(128))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=True) 
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.id'), nullable=True)
    realisation_id = db.Column(db.Integer, db.ForeignKey('realisation.id'), nullable=True) 
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True) 


    def __repr__(self):
        return ' {} '.format(self.url_img)


class Visiteur(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre_vis=db.Column(db.Integer, default=0)
    date_vist=db.Column(db.Date)
    
    def __repr__(self):
        return ' {} '.format(self.nombre_vis)



class Organisation (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    logo = db.Column(db.String(200), default='logo.png')
    adresse_mail = db.Column(db.Text)
    adresse_physique=db.Column(db.String(250))
    personnalite_juridique=db.Column(db.String(128))
    num_telephone=db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)

    def __repr__(self):
        return ' {} '.format(self.nom)


class Rubrique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    resume = db.Column(db.Text)
    image_rubrique = db.Column(db.String(200), default='image.jpg')
    statut = db.Column(db.Boolean, default=False)  
    donations = db.relationship('Donation', backref='donation_rub', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rubrique_id = db.Column(db.Integer, db.ForeignKey('rubrique.id'), nullable=True) 
    parrainage_id = db.Column(db.Integer, db.ForeignKey('parrainage.id'), nullable=True) 
    somme=db.Column(db.DECIMAL(precision=10, scale=2))
    noms = db.Column(db.String(128))
    resume = db.Column(db.Text)
    date_payements=db.Column(db.Date)
    identi_payement=db.Column(db.String(128))
    adresse=db.Column(db.String(128))
    email=db.Column(db.String(128))
    pays=db.Column(db.String(128))
    telephone=db.Column(db.String(128))

    def __repr__(self):
        return ' {} '.format(self.noms)

class Parrainage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noms = db.Column(db.String(128))
    resume = db.Column(db.Text)
    parrainage=db.Column(db.DECIMAL(precision=10, scale=2))
    date_de_naissance=db.Column(db.Date)
    image_rubrique = db.Column(db.String(200), default='image.jpg')
    statut = db.Column(db.Boolean, default=False)  
    donations = db.relationship('Donation', backref='donation_parrainage', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)
