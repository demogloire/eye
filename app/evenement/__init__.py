from flask import Blueprint

evenement = Blueprint('evenement', __name__, url_prefix='/event')
# never forget 
from . import routes