from django.forms import ModelForm
from core.svg import SvgAndImageFormField


class ArticleListItemForm(ModelForm):
    image = SvgAndImageFormField()
