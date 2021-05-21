from flask import Blueprint

categorie = Blueprint('categorie', __name__, url_prefix='/categorie')
# never forget 
from . import routes