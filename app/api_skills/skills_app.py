from flask import Blueprint,render_template,request,redirect,flash
from api_skills.skills_service import pagination_skills,delete_skill_by_id,add_skill
from service import login_required,redirect_last_url,edit_picture

skills_app=Blueprint("skills_app",__name__)

@skills_app.route("/",methods=['get','post'])
@login_required
def skills_index():
    filter=request.args.get("q")    
    pagination_list=pagination_skills(request=request,rows_per_pages=25,filter=filter)
    return render_template("/pages/skills.html",skills=pagination_list,picture_form=edit_picture())

@skills_app.route("/delete/<id>")
@login_required
def delete(id):
    delete_skill_by_id(id)
    return redirect(redirect_last_url(request,default="skills_app.skills_index"))

@skills_app.route("add/<skill_name>")
@login_required
def add(skill_name):
    add_skill(skill_name)
