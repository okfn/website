from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import models


class PublishedPressReleaseManager(models.Manager):
    def get_queryset(self):
        return super(PublishedPressReleaseManager, self).get_queryset().filter(
            release_date__lt=timezone.now())


class PressRelease(models.Model):
    objects = models.Manager()
    published_objects = PublishedPressReleaseManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    release_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('press-release', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-release_date',)


class PublishedPressMentionMananger(models.Manager):
    def get_queryset(self):
        return super(PublishedPressMentionMananger, self).get_queryset(). \
            filter(published=True)


class PressMention(models.Model):
    objects = models.Manager()
    published_objects = PublishedPressMentionMananger()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    publisher = models.CharField(max_length=60)
    publication_date = models.DateField()
    url = models.URLField()
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    notes = models.TextField()
    published = models.BooleanField()

    # TODO: add a projects FK.

    def get_absolute_url(self):
        return reverse('press-mention', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-publication_date',)
