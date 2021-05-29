from flask import Blueprint

parrainage = Blueprint('parrainage', __name__, url_prefix='/parrainage')
# never forget 
from . import routes