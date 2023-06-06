from django.forms import ModelForm
from core.svg import SvgAndImageFormField


class OKImageForm(ModelForm):
    image_url = SvgAndImageFormField()
