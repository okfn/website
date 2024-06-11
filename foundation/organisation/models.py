import logging
from hashlib import md5

from cms.models.pluginmodel import CMSPlugin
from cms.extensions import PageExtension
from django.db import models


logger = logging.getLogger(__name__)


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    username_on_slack = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to="organisation/people/photos", blank=True)
    twitter = models.CharField(max_length=18, blank=True)
    url = models.URLField(blank=True)

    NOWDOING_DEFAULT_ORDER = (
        "working",
        "location",
        "reading",
        "listening",
        "watching",
        "eating",
    )

    def __str__(self):
        return self.name

    @property
    def gravatar_url(self):
        """Returns the gravatar url for this user (constructed from email)"""
        base = "https://gravatar.com/avatar/{hash}?s=132"
        md5_hash = md5(self.email.strip().lower().encode("utf-8")).hexdigest()
        return base.format(hash=md5_hash)

    @property
    def nowdoing_with_latest(self):
        """All NowDoing attributes of the user with the most recently
        updated one marked with `is_newest_update`"""
        nowdoings = self.nowdoing_set.all().extra(order_by=["-updated_at"])
        if nowdoings:
            nowdoings[0].is_newest_update = True
        return nowdoings

    @property
    def nowdoing_by_custom_order(self, custom_order=None):
        custom_order = custom_order or self.NOWDOING_DEFAULT_ORDER
        nowdoings = self.nowdoing_with_latest
        ordered_nowdoings = list()
        for doing_type in custom_order:
            if nowdoings.filter(doing_type=doing_type):
                ordered_nowdoings.append(
                    nowdoings.filter(doing_type=doing_type).first()
                )
        return ordered_nowdoings

    @property
    def has_anything_to_show(self):
        """Is there anything that we can show for this person in the
        template (other then email which is checked separately)"""
        return self.url or self.twitter or self.nowdoing_set.count()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "people"


class NowDoing(models.Model):
    ACTIVITIES = (
        ("reading", "reading"),
        ("listening", "listening"),
        ("working", "working"),
        ("location", "location"),
        ("watching", "watching"),
        ("eating", "eating"),
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    doing_type = models.CharField(max_length=10, choices=ACTIVITIES)
    link = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def icon_name(self):
        """The name of the corresponding css icon class"""
        matching = {"watching": "playing"}
        return matching.get(self.doing_type, self.doing_type)

    @property
    def display_name(self):
        """The human readable string to be displayed in templates"""
        matching = {
            "reading": "Reading",
            "listening": "Listening to",
            "working": "Working on",
            "location": "Location",
            "watching": "Watching",
            "eating": "Eating",
        }
        return matching.get(self.doing_type, self.doing_type)

    def __repr__(self):
        return "<NowDoing: {}, {}>".format(self.person.name, self.doing_type)


class SignupForm(CMSPlugin):
    title = models.CharField(max_length=50, default="Get Connected to Open Knowledge")
    description = models.TextField(blank=True)


class SideBarExtension(PageExtension):
    enabled = models.BooleanField(default=True)
    image = models.ImageField(upload_to="organisation/sidebar/images", blank=True)
