from django.db import models
from pagedown.widgets import AdminPagedownWidget

class Job(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    submission_email = models.EmailField()
    submission_closes = models.DateTimeField()

    class Meta:
        ordering = ('submission_closes',)
