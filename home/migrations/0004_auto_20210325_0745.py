# Generated by Django 3.1.1 on 2021-03-25 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210321_1801'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='chargecode',
            name='billable',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
