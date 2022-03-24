from flask import (Blueprint, abort, redirect, render_template, request,session, url_for,jsonify)
from sqlalchemy import modifier
from service import login_required,edit_picture, super_admin_required
from admin.auth_service import (end_session, start_session,update_admin,admins_list,
                                addAdmin,deleteAdmin,update_super_admin,get_admin_by_id,update_admin_by_sa)
from admin.forms.login_form import LoginForm
from admin.forms.editAcc_form import EditProfile
from admin.forms.add_admin_form import AddAdminForm
from admin.forms.editAdmin_form import EditAdminForm


auth_app=Blueprint("auth_app",__name__)

@auth_app.route("/login",methods=["GET","POST"])
def login():
    if not session.get("logged"):
        form=LoginForm()
        if form.validate_on_submit():
            email=form.email.data
            password=form.password.data
            if start_session(email,password):
                return redirect(url_for("index"))
            print(form.errors)
        return render_template("pages/login.html",form=form)
    return redirect(url_for("index"))


@auth_app.route('/logout')
@login_required
def logout():
    end_session()
    return  redirect(url_for("auth_app.login"))


@auth_app.route("/profile",methods=['POST','GET'])
@login_required
def profile():
    edit_form=EditProfile()
    
    modification=False
    if edit_form.validate_on_submit():
        if session.get("role")=="admin":
            edit_form.email.data=session.get("email")
            edit_form.position.data=session.get("position")
            update_admin(username=edit_form.username.data,email=edit_form.email.data,password=edit_form.newPassword.data)
        else:
            update_super_admin(username=edit_form.username.data,email=edit_form.email.data,\
                    position=edit_form.position.data,password=edit_form.newPassword.data)
        modification=True
    return render_template("pages/edit_profile.html",\
        picture_form=edit_picture(),edit_form=edit_form,modification=modification)

@auth_app.route('/admins',methods=['get','post'])
@super_admin_required
def admins():
    return render_template("/pages/admins.html",\
        admins=admins_list(),\
        picture_form=edit_picture())

    
@auth_app.route("/ajouter_admin",methods=['POST','GET'])
@super_admin_required
def add_admin():
    addForm=AddAdminForm()
    added=False
    if addForm.validate_on_submit() :
        addAdmin(username=addForm.username.data,email=addForm.email.data,\
            password=addForm.password.data,position=addForm.position.data,\
                role=addForm.role.data)
        added=True
    return render_template("pages/add_admin.html",\
        addForm=addForm,\
        picture_form=edit_picture(),added=added)

@auth_app.route("/delete_admin/<id>",methods=["post"])
@super_admin_required
def delete_admin(id):
    deleteAdmin(id)
    return redirect(url_for('auth_app.admins'))


@auth_app.route("/edit_admin/<id>",methods=['post',"get"])
@super_admin_required
def edit_admin(id):
    try:
        modified=False
        adminEntity=get_admin_by_id(id)
        edit_admin=EditAdminForm()
        """edit_admin.email.data,edit_admin.username.data,edit_admin.position.data=\
            adminEntity.email,adminEntity.username,adminEntity.position"""
        if edit_admin.validate_on_submit():
            update_admin_by_sa(id=adminEntity.id_admin,username=edit_admin.username.data,\
            email=edit_admin.email.data,role=edit_admin.role.data,position=edit_admin.position.data)
            modified=True
        return render_template("/pages/edit_admin.html",adminEntity=adminEntity,edit_admin_form=edit_admin,\
            modification=modified,picture_form=edit_picture())
    except Exception as ex:
        return str(ex)
        return abort(404)
    