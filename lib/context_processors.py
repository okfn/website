from django.contrib.sites.models import Site

def site_processor(request):
    return { 'site': Site.objects.get_current() }
