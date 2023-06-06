from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class ArticleLinkForm(ModelForm):
    image = SvgAndImageFormField()
