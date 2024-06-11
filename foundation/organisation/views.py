from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from .models import Person


class PersonView(DetailView):
    model = Person
    template_name = 'organisation/member_detail.html'

    def get_object(self, *args, **kwargs):
        person_id = self.kwargs.get('person_id', '')
        return get_object_or_404(Person, id=person_id)
