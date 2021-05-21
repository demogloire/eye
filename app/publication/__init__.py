from flask import Blueprint

publication = Blueprint('publication', __name__, url_prefix='/publication')
# never forget 
from . import routes