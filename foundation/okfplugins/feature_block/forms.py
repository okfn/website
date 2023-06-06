from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class FeatureBlockForm(ModelForm):
    image = SvgAndImageFormField()
