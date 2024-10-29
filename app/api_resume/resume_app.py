from flask import (Blueprint, render_template, redirect, url_for)
from service import login_required, redirect_last_url, edit_picture
from .forms.upload_cv_form import UploadResume
from .forms.filter_cv_form import FilterCvForm
from .services.resume_service import (resume_add, resume_del, get_all_countries_cvs,
                                      get_all_education_cvs, get_all_skills_cvs, get_languages)
from config import Config
from models.resumeEntity import Resume, db, Education,Skill
from time import time
from sqlalchemy import desc
from flask import request
from sqlalchemy import and_, or_


resume_app = Blueprint("resume_app", __name__)


@resume_app.route("/", methods=["post", "get"])
@login_required
def resumes():
    cvs_info = {
        "skills": get_all_skills_cvs(),
        "educations": get_all_education_cvs(),
        "countries": get_all_countries_cvs(),
        "languages": get_languages()
    }
    upload_form = UploadResume()
    filter_form = FilterCvForm(
        skills_choices=cvs_info.get("skills"),
        education_choices=cvs_info.get("educations"),
        country_choices=cvs_info.get("countries"),
        langue_choices=cvs_info.get("languages"),
        args=request.args
    )
    
    if upload_form.validate_on_submit():
        for file in upload_form.files.data:
            success = resume_add(file)
            if not success:
                # Handle upload failure, e.g., flash a message
                pass
    
    if filter_form.validate_on_submit():
        try:
            filtred_res = Resume.query
            if filter_form.education.data:
                filtred_res = filtred_res.filter(Resume.educations.any(Education.degree.in_(filter_form.education.data)))
            if filter_form.langue.data:
                filtred_res = filtred_res.filter(Resume.language.in_(filter_form.langue.data))
            if filter_form.country.data:
                filtred_res = filtred_res.filter(Resume.country.in_(filter_form.country.data))
            if filter_form.skill.data:
                filtred_res = filtred_res.filter(Resume.skills.any(Skill.skill_name.in_(filter_form.skill.data)))
            
            resumes = filtred_res.order_by(desc(Resume.id_resume)).all()
        except Exception as e:
            print(f"Error during filtering: {e}")
            resumes = Resume.query.order_by(desc(Resume.id_resume)).all()
    else:
        resumes = Resume.query.order_by(desc(Resume.id_resume)).all()
    
    return render_template(
        "pages/resumes.html",
        upload_form=upload_form,
        resumes=resumes,
        picture_form=edit_picture(),
        filter_form=filter_form,
        cvs_info=cvs_info
    )

@ resume_app.route("/delete/<id>", methods=["post", "get"])
@ login_required
def delete(id):
    resume_del(id)
    return redirect(redirect_last_url(request))
