import os
import smtplib
from flask import Flask, render_template, abort, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import flask_sijax


#Importation des configuration de l'application sur le developpement de l'application
from config import app_config



account_sid = 'AC6ae3e81d9f78448d62d93da0f6ebad34'
auth_token = '21aedb0020969d30b4e7d16629fd3c4d'

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
#Structure de l'application

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')


def create_app (config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile( 'config.py')

    #Cloudinary
    app.config.from_mapping(
        CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL') or 'Pegue a sua Key',
    )
      
    # #Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
  
    
    #Sijax
    app.config['SIJAX_STATIC_PATH'] = path
    app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
    flask_sijax.Sijax(app)

    login_manager.login_message = "Veuillez vous connecté"
    login_manager.login_view = "auth.login"
    login_manager.login_message_category ='danger'
    #SimpleMDE(app)

    #md= Markdown(app, extensions=['fenced_code'])
    from app import models
       

    ''' 
    Utilisation des stucture Blueprint
    '''

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page non trouvée'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Erreur serveur'), 500
    
    #Authentification
    from .authentification import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .categorie import categorie as categorie_blueprint
    app.register_blueprint(categorie_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .publication import publication as publication_blueprint
    app.register_blueprint(publication_blueprint)

    from .cbca import cbca as cbca_blueprint
    app.register_blueprint(cbca_blueprint)
    
    from .album import album as album_blueprint
    app.register_blueprint(album_blueprint)

    from .evenement import evenement as evenement_blueprint
    app.register_blueprint(evenement_blueprint)

    from .realisation import realisation as realisation_blueprint
    app.register_blueprint(realisation_blueprint)

    from .media import media as media_blueprint
    app.register_blueprint(media_blueprint)

    from .organisation import organisation as organisation_blueprint
    app.register_blueprint(organisation_blueprint)
    
    from .event import event as event_blueprint
    app.register_blueprint(event_blueprint)


    from .autorisation import autorisation as autorisation_blueprint
    app.register_blueprint(autorisation_blueprint)
    
    from .statistique import stat as stat_blueprint
    app.register_blueprint(stat_blueprint)
    
    return app

   
