from flask import Blueprint

event = Blueprint('event', __name__, url_prefix='/event')
# never forget 
from . import routes