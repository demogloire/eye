from flask import Blueprint

stat = Blueprint('stat', __name__, url_prefix='/stat')
# never forget 
from . import routes