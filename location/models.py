from django.db import models
from wagtail.snippets.models import register_snippet
# Create your models here.
@register_snippet
class TaxLocation(models.Model):
    abbreviation = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    def __str__(self):
        return self.abbreviation