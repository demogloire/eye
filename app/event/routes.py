import socket
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import event
from ..utilites.utility import user_mac



@event.route("/")
@login_required
def index():
    return render_template('event/index.html',title="Dashboard")

@event.route("/ajouter")
@login_required
def ajouter():
    return render_template('event/ajouter.html',title="Dashboard")





