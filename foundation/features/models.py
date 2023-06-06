from django.db import models


class Feature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='features/images', blank=False)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=100, blank=False, null=False)
    published = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "features"
