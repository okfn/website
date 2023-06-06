from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class OKImageForm(ModelForm):
    image_url = SvgAndImageFormField()
