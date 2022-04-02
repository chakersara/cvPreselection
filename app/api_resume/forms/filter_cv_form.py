from flask_wtf import FlaskForm
from wtforms import SelectMultipleField
from models.resumeEntity  import Education


class FilterCvForm(FlaskForm):
    langue=SelectMultipleField("langue",choices=[("fr","Français"),("en","Anglais")])
