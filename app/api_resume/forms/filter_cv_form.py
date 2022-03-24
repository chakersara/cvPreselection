from flask_wtf import FlaskForm
from wtforms import SelectMultipleField
from ...models.resumeEntity import Education


class FilterCvForm(FlaskForm):
    education = SelectMultipleField(
        "education", choices=[(educ.degree, educ.degree) for educ in Education.query.all()])
    langue=SelectMultipleField("langue",choices=[("fr","Français"),("en","Anglais")])
