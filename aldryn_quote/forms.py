from django import forms
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from .models import Quote


class QuotePluginForm(forms.ModelForm):
    model = Quote

    def clean_style(self):
        style = self.cleaned_data.get('style')
        # Check if template for style exists:
        try:
            select_template(['aldryn_quote/plugins/%s/quote.html' % style])
        except TemplateDoesNotExist:
            raise forms.ValidationError(_('Template not found'))
        return style
