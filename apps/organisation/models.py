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

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


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
    description = models.TextField()

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
