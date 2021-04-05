from django.db import models
from wagtail.snippets.models import register_snippet
from account.models import Profile

# Create your models here.
@register_snippet
class ChargeCode(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ManyToManyField(Profile)
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=60)
    color = models.CharField(max_length=10, null=True, blank=True)
    bgColor = models.CharField(max_length=10, null=True, blank=True)
    dragBgColor = models.CharField(max_length=10, null=True, blank=True)
    borderColor = models.CharField(max_length=10, null=True, blank=True)
    personal_list = models.BooleanField(default=False, null=True, blank=True)
    

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def __str__(self):
        return self.name