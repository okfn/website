from django.forms import ModelForm
from core.svg import SvgAndImageFormField


class VideoForm(ModelForm):
    video_image = SvgAndImageFormField()
