from cms.models.pluginmodel import CMSPlugin
from django.db import models


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

    theme = models.ForeignKey('Theme', blank=True)

    incubation = models.BooleanField(default=True,
                                     help_text='Is this group in incubation?')

    def __unicode__(self):
        return self.name


class FeaturedProject(CMSPlugin):
    project = models.ForeignKey('Project', related_name='+')

    def __unicode__(self):
        return self.project.name
