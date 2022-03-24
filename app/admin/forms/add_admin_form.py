from flask_wtf import FlaskForm
from wtforms import TextField,RadioField,SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from admin.auth_service import all_admin_emails,all_admin_usernames
from string import punctuation

class AddAdminForm(FlaskForm):
    username=TextField("username",validators=[DataRequired("Veuillez choisir un nom d'utilisateur"),\
        Length(min=5,message="La longeur du nom d'utilisateur doit être supérieur ou égal à 5")])
    email=StringField('email',validators=[DataRequired('Veuillez saisir une adresse email'),\
        Email('Veuillez saisir une adresse email valide')])
    position=StringField('position',validators=[DataRequired("Veuillez saisir la position de travail")])
    role=RadioField("role",choices=[("admin","Administrateur"),("super_admin","Super Administrateur")],\
        validators=[DataRequired("Veuillez choisir un rôle pour l'administrateur")])
    password=PasswordField('password',validators=[DataRequired("Veuillez saisir un mot de passe"),\
        Length(min=8,message="Le mot de passe doit être supérieur ou égal à 8 caractères et doit contenir au moins un caractère spécial")])
    confirmPassword=PasswordField('comfirm_password',validators=[DataRequired("Veuillez resaisir le mot de passe"),EqualTo('password',message='Les deux mots de passe doivent être identiques')])
    submit=SubmitField("submit")

    def validate_username(self,username):
        if self.username.data in all_admin_usernames():
            raise ValidationError("Nom d'utilisateur utilisé")
        
    def validate_email(self,email):
        if self.email.data in all_admin_emails():
            raise ValidationError("Adresse email utiliséé")

    def validate_password(self,password):
        if len(self.password.data)>=8 and not set(punctuation).intersection(self.password.data):
            raise ValidationError('Le mot de passe doit être supérieur ou égal à 8 caractères et doit contenir au moins un caractère spécial.')

