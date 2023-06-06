from django.forms import ModelForm
from foundation.core.svg import SvgAndImageFormField


class ArticleListItemForm(ModelForm):
    image = SvgAndImageFormField()
