# Generated by Django 3.1.1 on 2021-03-25 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210325_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chargecode',
            name='billable',
        ),
        migrations.AddField(
            model_name='taskauthorization',
            name='billable',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]