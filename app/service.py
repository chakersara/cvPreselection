import os
from admin.auth_service import return_admin,update_image
from functools import wraps
from pathlib import Path
from random import randint
from flask import url_for,redirect,session,request
from admin.forms.editAcc_form import PictureForm
from werkzeug.utils import secure_filename
from models import db
from flask import request
from models.adminEntity import Admin


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth_app.login'))
    return wrap


def super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("role")=="super_admin" and 'logged' in session :
            return f(*args, **kwargs)
        else:
            return redirect(redirect_last_url(request))
    return wrap



def redirect_last_url(request,default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def path_to_save_images():
    return '{}/{}'.format(str(Path(__file__)).split("/app")[0],"app/static/images/users")

def edit_picture():
    form=PictureForm()
    if form.validate_on_submit():
        f=form.photo.data
        file_name=secure_filename(session.get("username")+str(randint(1,89))+f.filename)
        f.save(os.path.join(
            path_to_save_images(), '', file_name
        ))
        update_image(session["email"],file_name)
    return form
