from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def active_release(release_date):
    try:
        week_ago = timezone.now() - timedelta(weeks=1)
        return release_date > week_ago
    except:
        return False
