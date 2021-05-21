from flask import Blueprint

realisation = Blueprint('realisation', __name__, url_prefix='/realisation')
# never forget 
from . import routes