from flask import Blueprint

projet = Blueprint('projet', __name__, url_prefix='/')
# never forget 
from . import routes