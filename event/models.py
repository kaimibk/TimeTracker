from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet
from django.conf import settings
from category.models import Category
from taskauthorization.models import TaskAuthorization

# Create your models here.
@register_snippet
class Event(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255, null=True, blank=True)
    isAllDay = models.BooleanField(default=False)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    delta_time = models.FloatField(null=True, blank=True)
    # TODO: change to relation
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    dueDateClass = models.CharField(max_length=25, null=True, blank=True)    
    # TODO: Change to relation
    # charge_code = models.ForeignKey(ChargeCode, null=True, blank=True, on_delete=models.CASCADE)
    task_authorization = models.ForeignKey(TaskAuthorization, null=True, blank=True, on_delete=models.CASCADE)

    location = models.CharField(max_length=100, null=True, blank=True)
    # TODO: Change to choice fields
    event_type = models.CharField(null=True, blank=True, max_length=100)
    notes = RichTextField(null=True, blank=True)
    #telework = models.BooleanField(default=False, null=True, blank=True)
    #tax_location = foreign key to TaxLocation
    def __str__(self):
        return self.title