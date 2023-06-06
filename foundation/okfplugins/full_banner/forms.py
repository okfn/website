from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class FullBannerForm(ModelForm):
    banner_background = SvgAndImageFormField()
    banner_picture = SvgAndImageFormField()
