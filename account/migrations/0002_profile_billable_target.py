# Generated by Django 3.1.1 on 2021-03-21 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='billable_target',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
