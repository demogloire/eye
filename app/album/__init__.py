from flask import Blueprint

album = Blueprint('album', __name__, url_prefix='/album')
# never forget 
from . import routes