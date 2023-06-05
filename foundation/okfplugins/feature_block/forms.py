from django.forms import ModelForm
from core.svg import SvgAndImageFormField


class FeatureBlockForm(ModelForm):
    image = SvgAndImageFormField()
