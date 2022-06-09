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
