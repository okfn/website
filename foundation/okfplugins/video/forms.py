from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class VideoForm(ModelForm):
    video_image = SvgAndImageFormField()
