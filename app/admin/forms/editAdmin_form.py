from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,ValidationError,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import SubmitField,PasswordField,StringField,RadioField
from admin.auth_service import return_admin,check_username_exist,return_admin_byUsername
from string import punctuation
from flask import session


class EditAdminForm(FlaskForm):

    username=StringField('username', validators=[DataRequired("Veuillez choisir un nom d'utilisateur"),\
        Length(min=5,message="La longeur du nom d'utilisateur doit être supérieur ou égal à 5")])
    email=StringField('email',validators=[DataRequired("Veuillez saisir une adresse mail")])
    position=StringField('position',validators=[DataRequired("Veuillez saisir votre position de travail")])
    role=RadioField("role",choices=[("admin","Administrateur"),("super_admin","Super Administrateur")],\
        validators=[DataRequired("Veuillez choisir un rôle pour l'administrateur")])
    password=PasswordField('password',validators=[DataRequired("Veuillez saisir votre mot de passe")])
    submit=SubmitField("Enregistrer")


    def validate_email(self,email):
        adminEntity = return_admin_byUsername(self.username.data)
        if not(not check_username_exist(self.username.data) or self.username.data==adminEntity.username):
            raise ValidationError("Nom d'utilisateur invalide")
    

    def validate_password(self,password):
        super_admin_pass=return_admin(email=session['email']).password
        if not check_password_hash(super_admin_pass,self.password.data):
            raise ValidationError("Mot de passe incorrecte")
