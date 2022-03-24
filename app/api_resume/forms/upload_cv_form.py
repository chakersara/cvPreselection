from flask_wtf import FlaskForm
from wtforms import MultipleFileField,SubmitField
from flask_wtf.file import FileAllowed
from wtforms.validators import ValidationError

class UploadResume(FlaskForm):
    files=MultipleFileField('cvs')
    submit=SubmitField("Enregistrer")


    def validate_files(self,files):
        for file in self.files.data:
            if file.filename.split(".")[-1] not in ('pdf','doc','docx'):
                raise ValidationError("Seuls les fichiers pdf,doc et docx sont autorisés")
