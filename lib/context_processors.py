from django.conf import settings
from django.contrib.sites.models import Site


def site(request):
    host = request.get_host()
    if host in ["127.0.0.1:8000", "localhost:8000"]:
        environment = 'DEVELOP'
    elif host == "next.okfn.org":
        environment = 'STAGING'
    elif host == "okfn.org":
        environment = 'PRODUCTION'
    else:
        environment = 'UNKNOWN'

    return {
        'site': Site.objects.get_current(),
        'environment': environment,
        'host': host
    }


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


def mailchimp(request):
    """
    Add the Mailchimp mailing list url and token to the context for use when
    rendering signup forms.
    """
    return {
        'MAILCHIMP_URL': settings.MAILCHIMP_URL,
        'MAILCHIMP_TOKEN': settings.MAILCHIMP_TOKEN,
    }
