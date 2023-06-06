from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class HeaderForm(ModelForm):
    image = SvgAndImageFormField()
