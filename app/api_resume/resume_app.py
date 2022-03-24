from distutils.command.config import config
from random import randint
from flask import (Blueprint,render_template,redirect,url_for)
from service import login_required,redirect_last_url,edit_picture
from .forms.upload_cv_form import UploadResume
from .services.resume_service import resume_add,resume_del
from config import Config
from models.resumeEntity import Resume,db
import asyncio
from time import time
from sqlalchemy import desc
from flask import request


resume_app=Blueprint("resume_app",__name__)

@resume_app.route("/",methods=["post","get"])
@login_required
def resumes():
    upload_form=UploadResume()
    if upload_form.validate_on_submit():
        for file in upload_form.files.data:
            resume_add(file)
    resumes=Resume.query.order_by(desc(Resume.id_resume)).all()
    db.session.commit()
    return render_template("pages/resumes.html",upload_form=upload_form,\
        resumes=resumes,picture_form=edit_picture())

@resume_app.route("/delete/<id>",methods=["post","get"])
@login_required
def delete(id):
    resume_del(id)
    return redirect(redirect_last_url(request))


"""@resume_app.route("/haha",methods=['get','post'])
async def get_data():
    start=time()
    upload_form=UploadResume()
    if upload_form.validate_on_submit():
        for file in upload_form.files.data:
            await resume_add(file)
    resumes=Resume.query.all()
    end=time()
    print(f"with async {end-start}")
    return render_template("pages/resumes.html",upload_form=upload_form,\
        resumes=resumes,picture_form=edit_picture())"""

