from django.conf import settings
from django.contrib.sites.models import Site


def site(request):
    return {'site': Site.objects.get_current()}


def google_analytics(request):
    """
    Add the Google Analytics tracking ID and domain to the context for use when
    rendering tracking code.
    """
    ga_tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and ga_tracking_id and ga_domain:
        return {
            'GOOGLE_ANALYTICS_TRACKING_ID': ga_tracking_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}


def sendy(request):
    """
    Add the Sendy mailing list token to the context for use when rendering
    signup forms.
    """
    return {
        'SENDY_URL': settings.SENDY_URL,
        'SENDY_TOKEN': settings.SENDY_TOKEN,
    }
