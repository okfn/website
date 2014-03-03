from django.test import TestCase

from ..models import Person
from ..search_indexes import PersonIndex


class PersonIndexTest(TestCase):
    def setUp(self):  # flake8: noqa
        self.leonardo = Person.objects.create(
            name="Leonardo (Leo)",
            description='Turtle with a blue mask',
            email='leonardo@tmnt.org')

    def test_queryset_includes_person(self):
        index = PersonIndex()

        self.assertIn(self.leonardo, index.index_queryset())
