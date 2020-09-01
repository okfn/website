from django.utils.timezone import now
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from .utils import get_additional_styles

# Create your models here.
class Quote(CMSPlugin):
    """
    A quote or testimonial
    """
    STANDARD = 'standard'

    STYLE_CHOICES = [
        (STANDARD, _('Standard')),
    ]

    style = models.CharField(_('Style'), choices=STYLE_CHOICES + get_additional_styles(), default=STANDARD, max_length=50)
    created_at = models.DateTimeField(_('Created at'), default=now)
    content = models.TextField(_('Quote'), default='')
    footer = models.TextField(_('Footer'), blank=True)
    url = models.URLField(_('Link'), blank=True)
    target = models.CharField(_('Target'), max_length=50, blank=True, default='_blank', choices=(('_blank',  _('New window')),))

    def __unicode__(self):
        return self.content[:50]