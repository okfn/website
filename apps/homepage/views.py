from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'homepage/home.html'

homepage = HomepageView.as_view()
