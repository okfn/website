from django.db import models


class PressRelease(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    body = models.TextField()
    release_date = models.DateTimeField()
    published = models.BooleanField()

    class Meta:
        ordering = ('-release_date',)


class PressMention(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    publisher = models.CharField(max_length=60)
    publication_date = models.DateField()
    url = models.URLField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    notes = models.TextField()

    # TODO: add a projects FK.

    class Meta:
        ordering = ('-publication_date',)
