from django.db import models
from ..background.models import AbstractBackgroundPlugin


class Carousel(AbstractBackgroundPlugin):
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.title
