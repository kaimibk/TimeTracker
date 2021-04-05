from django.db import models
from wagtail.snippets.models import register_snippet
# Create your models here.
@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'