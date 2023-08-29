from django.db import models
from ..background.models import AbstractBackgroundPlugin


class Gallery(AbstractBackgroundPlugin):
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
