from flask import Blueprint

cbca = Blueprint('cbca', __name__, url_prefix='/')
# never forget 
from . import routes