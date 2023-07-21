from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class PersonForm(ModelForm):
    photo = SvgAndImageFormField()

