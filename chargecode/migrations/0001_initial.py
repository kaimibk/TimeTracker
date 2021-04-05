# Generated by Django 3.1.1 on 2021-04-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_profile_billable_target'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('code', models.CharField(max_length=60)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('bgColor', models.CharField(blank=True, max_length=10, null=True)),
                ('dragBgColor', models.CharField(blank=True, max_length=10, null=True)),
                ('borderColor', models.CharField(blank=True, max_length=10, null=True)),
                ('personal_list', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ManyToManyField(to='account.Profile')),
            ],
        ),
    ]
