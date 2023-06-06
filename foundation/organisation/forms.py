from django.forms import ModelForm
from core.svg import SvgAndImageFormField


class PersonForm(ModelForm):
    photo = SvgAndImageFormField()


class ProjectForm(ModelForm):
    picture = SvgAndImageFormField()


class ThemeForm(ModelForm):
    picture = SvgAndImageFormField()


class WorkingGroupForm(ModelForm):
    logo = SvgAndImageFormField()
