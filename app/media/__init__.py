from flask import Blueprint

media = Blueprint('media', __name__, url_prefix='/media')
# never forget 
from . import routes