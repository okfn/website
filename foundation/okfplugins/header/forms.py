from django.forms import ModelForm
from core.svg import SvgAndImageFormField


class HeaderForm(ModelForm):
    image = SvgAndImageFormField()
