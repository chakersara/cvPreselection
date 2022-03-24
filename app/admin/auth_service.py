from models.adminEntity import Admin
from models import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from pathlib import Path


def addAdmin(username,email,password,position,role="admin"):
    if session.get("logged") and session.get("role")=='super_admin':
        adminEntity=Admin(username=username,email=email,password=generate_password_hash(password),role=role,position=position)
        db.session.add(adminEntity)
        db.session.commit()
        return True
    return False


def return_admin(email):
    return Admin.query.filter(Admin.email==email).first()

def return_admin_byUsername(username):
    return Admin.query.filter(Admin.username==username).first()


def admins_list():
    return Admin.query.all()

def all_admin_usernames():
    return tuple(map(lambda user:user[0],Admin.query.with_entities(Admin.username).all()))

def all_admin_emails():
    return tuple(map(lambda email:email[0],Admin.query.with_entities(Admin.email).all()))

def update_image(email,image):
    admin=return_admin(email)
    admin.image=image
    session['image']=image
    db.session.commit()

def update_admin(username,email,password):
    admin=return_admin(email)
    admin.username=username
    if password :
        admin.password=password
    session['username']=admin.username
    db.session.commit()

def get_admin_by_id(id):
    return Admin.query.get(id)

def update_admin_by_sa(id,username,email,role,position):
    adminEntity=get_admin_by_id(id)
    adminEntity.email=email
    adminEntity.role=role
    adminEntity.position=position
    if id==session.get('id'):
        adminEntity.username=username
        session['username']=adminEntity.username
        session['email']=adminEntity.email
        session['position']=adminEntity.position
        db.session.commit()


def update_super_admin(username,email,position,password):
    admin=return_admin(email)
    admin.username,admin.email,admin.position=username,email,position
    if password :
        admin.password=password
    session['username']=admin.username
    session['email']=admin.email
    session['position']=admin.position
    session['id']=admin.id_admin
    db.session.commit()

def deleteAdmin(id_admin):
    try:
        adminEntity=Admin.query.filter(Admin.id_admin==id_admin).first()
        db.session.delete(adminEntity)
        db.session.commit()
    except:
        pass

def check_admin(email,password):
    try:
        get_password=return_admin(email=email).password
        if check_password_hash(get_password,password):
            
            return True
        return False
    except:
        return False

def check_username_exist(username):
    return True if Admin.query.filter(Admin.username==username).first() else False


def check_email_exist(email):
    return True if Admin.query.filter(Admin.email==email).first() else False

def save_session(id,username,email,role,image,position):
    session.setdefault("logged",True)
    session.setdefault("username",username)
    session.setdefault("email",email)
    session.setdefault("role",role)
    session.setdefault("image",image)
    session.setdefault("position",position)
    session.setdefault("id",id)

def start_session(email,password):
    if check_admin(email,password):
        adminEntity=return_admin(email)
        save_session(id=adminEntity.id_admin,username=adminEntity.username,email=adminEntity.email,
        role=adminEntity.role,image=adminEntity.image,position=adminEntity.position)
        return True
    return False



def end_session():
    session.clear()

