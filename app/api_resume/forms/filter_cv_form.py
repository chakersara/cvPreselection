from typing import List
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FilterCvForm(FlaskForm):
    def __init__(self, langue_choices, education_choices, skills_choices, country_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.langue.choices = langue_choices
        self.education.choices = education_choices
        self.skill.choices = skills_choices
        self.country.choices = country_choices

    langue = MultiCheckboxField("langue", choices=[])
    education = MultiCheckboxField("education", choices=[])
    skill = MultiCheckboxField("skill", choices=[])
    country = MultiCheckboxField("country", choices=[])
