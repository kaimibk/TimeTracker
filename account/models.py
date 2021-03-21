from django.db import models
from django.db.models.signals import post_save
from django import forms
from django.dispatch import receiver
from django.contrib.auth.models import User
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    pto_balance = models.FloatField(null=True, blank=True)
    billable_target = models.FloatField(null=True, blank=True)

    panels = [
        FieldPanel("user", widget=forms.Select),
        FieldPanel("email", widget=forms.EmailInput),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("pto_balance"),
        FieldPanel("billable_target"),
    ]

    def __str__(self):
        return f"({self.user.username}) {self.first_name} {self.last_name}"

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()