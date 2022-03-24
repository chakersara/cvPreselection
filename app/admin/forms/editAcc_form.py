from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,ValidationError,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import SubmitField,PasswordField,StringField
from admin.auth_service import return_admin,check_username_exist
from string import punctuation
from flask import session

class PictureForm(FlaskForm):
    photo=FileField('photo',validators=[FileRequired(),FileAllowed(['jpg','png','gif','svg','jpeg'],message="Seules les images sont autorisées")])
    submit=SubmitField('Enregistrer')


class EditProfile(FlaskForm):

    username=StringField('username', validators=[DataRequired("Veuillez choisir un nom d'utilisateur"),\
        Length(min=5,message="La longeur du nom d'utilisateur doit être supérieur ou égal à 5")])
    email=StringField('email',validators=[DataRequired("Veuillez saisir une adresse mail")])
    position=StringField('position',validators=[DataRequired("Veuillez saisir votre position de travail")])
    password=PasswordField('password',validators=[DataRequired("Veuillez saisir votre mot de passe")])
    newPassword=PasswordField('new_password')
    confirmPassword=PasswordField('comfirm_password',validators=[EqualTo('newPassword',message='Les deux mots de passe doivent être identiques')])
    submit=SubmitField("Enregistrer")


    def validate_password(self,password):
        adminEntity = return_admin(email=session['email'])
        if not check_password_hash(adminEntity.password,self.password.data):
            raise ValidationError('Votre mot de passe est incorrecte')
      

    def validate_username(self,username):
        adminEntity = return_admin(email=session['email'])
        if not(not check_username_exist(self.username.data) or self.username.data==adminEntity.username):
            raise ValidationError("Nom d'utilisateur invalide")
    
    def validate_newPassword(self,newPassword):
        if self.newPassword.data:
            if not set(punctuation).intersection(self.newPassword.data):
                raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial")
    
    def validate_confirmPassword(self,confirmPassword):
        if self.newPassword.data:
            if len(self.newPassword.data)<8 and not set(punctuation).intersection(self.newPassword.data):
                raise ValidationError('Le mot de passe doit être supérieur ou égal à 8 caractères et doit contenir au moins un caractère spécial.')
           