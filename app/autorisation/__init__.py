from flask import Blueprint

autorisation = Blueprint('autorisation', __name__, url_prefix='/autorisation')
# never forget 
from . import routes