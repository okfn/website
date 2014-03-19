from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django_countries.fields import CountryField
from geoposition.fields import GeopositionField
from django.utils.text import slugify


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    photo = models.ImageField(upload_to='organisation/people/photos',
                              blank=True)
    twitter = models.CharField(max_length=18, blank=True)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "people"


class Unit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    members = models.ManyToManyField('Person', through='UnitMembership')
    order = models.IntegerField(
        blank=True, null=True,
        help_text="Higher numbers mean higher up in the food chain")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["-order", "name"]


class UnitMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    person = models.ForeignKey('Person')
    unit = models.ForeignKey('Unit')

    def __unicode__(self):
        return self.person.name + ' - ' + self.title


class Board(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    members = models.ManyToManyField('Person', through='BoardMembership')

    def __unicode__(self):
        return self.name


class BoardMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    person = models.ForeignKey('Person')
    board = models.ForeignKey('Board')

    def __unicode__(self):
        return self.person.name + ' - ' + self.title


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    teaser = models.CharField(
        max_length=100,
        help_text="A single line description for list views")
    description = models.TextField()
    picture = models.ImageField(upload_to='projects/pictures',
                                blank=True)

    twitter = models.CharField(max_length=18, blank=True)
    homepage_url = models.URLField(blank=True)
    sourcecode_url = models.URLField(blank=True)
    mailinglist_url = models.URLField(blank=True)

    themes = models.ManyToManyField('Theme', blank=True)
    types = models.ManyToManyField('ProjectType', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProjectType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Theme(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class WorkingGroupManager(models.Manager):

    def active(self):
        return self.get_queryset().filter(incubation=False)

    def incubators(self):
        return self.get_queryset().filter(incubation=True)


class WorkingGroup(models.Model):
    objects = WorkingGroupManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    description = models.TextField()
    url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organisation/working-groups/logos',
                             blank=True)

    theme = models.ForeignKey('Theme', blank=True, null=True)

    incubation = models.BooleanField(default=True,
                                     help_text='Is this group in incubation?')

    def __unicode__(self):
        return self.name


class NetworkGroupManager(models.Manager):

    def countries(self):
        return self.get_queryset().filter(region_slug__isnull=True)

    def regions(self, country):
        return self.get_queryset().filter(country_slug=country,
                                          region_slug__isnull=False)


class NetworkGroup(models.Model):
    objects = NetworkGroupManager()

    GROUP_TYPES = ((0, 'Local group'),
                   (1, 'Chapter'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)

    group_type = models.IntegerField(default=0, choices=GROUP_TYPES)
    description = models.TextField(blank=True, null=True)

    country = CountryField()
    country_slug = models.SlugField()
    region = models.CharField(max_length=100, blank=True, null=True)
    region_slug = models.SlugField(default=None, null=True)

    mailinglist = models.URLField(blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=18, blank=True, null=True)

    position = GeopositionField(blank=True, null=True)

    extra_information = models.TextField(blank=True, null=True)

    members = models.ManyToManyField('Person',
                                     through='NetworkGroupMembership')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.twitter.startswith('@'):
            self.twitter = self.twitter[1:]

        # Slug is either the country slugified or the region
        # Therefore we cannot force slug to be unique
        # (regions might have same name in different countries)
        self.country_slug = slugify(self.get_country_display())
        if self.region:
            self.region_slug = slugify(self.region)

        super(NetworkGroup, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('country', 'region')

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^geoposition\.fields\.GeopositionField"])


class NetworkGroupMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    networkgroup = models.ForeignKey('NetworkGroup')
    person = models.ForeignKey('Person')

    def __unicode__(self):
        return self.person.name + ' - ' + self.networkgroup.name


class FeaturedProject(CMSPlugin):
    project = models.ForeignKey('Project', related_name='+')

    def __unicode__(self):
        return self.project.name


class ProjectList(CMSPlugin):
    theme = models.ForeignKey(
        'Theme', blank=True, null=True,
        help_text='Limit to projects with this theme')
    project_type = models.ForeignKey(
        'ProjectType', blank=True, null=True,
        help_text='Limit to projects with this type')
