from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,Length,ValidationError
from admin.auth_service import check_email_exist,check_admin


class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(message='Veuillez saisir votre adresse e-mail'),Email("Email invalide")])
    password=PasswordField("Mot de passe",validators=[DataRequired("Veuillez saisir votre mot de passe")])
    submit=SubmitField('Connexion')

    def validate_email(self,email):
        if not check_email_exist(email=self.email.data):
            raise ValidationError(message='Adresse e-mail non trouvée')

    def validate_password(self,password):
        if check_email_exist(email=self.email.data) and not check_admin(email=self.email.data,password=self.password.data):
            raise ValidationError('Mot de passe incorrecte')