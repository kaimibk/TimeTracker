from django.db import models
from wagtail.snippets.models import register_snippet
from account.models import Profile
from chargecode.models import ChargeCode
# Create your models here.
@register_snippet
class TaskAuthorization(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hours_allocated = models.FloatField(default=1.0)
    hours_spent = models.FloatField(null=True, blank=True) #not sure
    hours_remaining = models.FloatField(null=True, blank=True) #not sure
    hours_percentage = models.FloatField(null=True, blank=True) #not sure
    billable_percentage = models.FloatField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    ta_file = models.FileField(null=True, blank=True)
    charge_code = models.ForeignKey(ChargeCode, null=True, blank=True, on_delete=models.CASCADE)
    is_billable = models.BooleanField(default=False, null=True, blank=True)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    # def hours_remaining(self):
    #     return self.hours_allocated - self.hours_spent

    # def hours_percentage(self):
    #     return self.hours_spent / self. hours_allocated
       
    def __str__(self):
        return f"{self.charge_code.name}_{self.start_date}_{self.end_date}_{self.user.email}"