from flask import Blueprint

organisation = Blueprint('organisation', __name__, url_prefix='/organisation')
# never forget 
from . import routes