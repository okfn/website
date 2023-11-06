from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class HeroPunchForm(ModelForm):
    image = SvgAndImageFormField()
