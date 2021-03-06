# Generated by Django 3.1.1 on 2021-03-21 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('account', '0002_profile_billable_target'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='TablesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('dbModel', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TaxLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(blank=True, max_length=10, null=True)),
                ('state', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='subheader',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TaskAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_allocated', models.FloatField(default=1.0)),
                ('hours_spent', models.FloatField(blank=True, null=True)),
                ('hours_remaining', models.FloatField(blank=True, null=True)),
                ('hours_percentage', models.FloatField(blank=True, null=True)),
                ('billable_percentage', models.FloatField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('ta_file', models.FileField(blank=True, null=True, upload_to='')),
                ('charge_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.chargecode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.CharField(blank=True, max_length=255, null=True)),
                ('isAllDay', models.BooleanField(default=False)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('delta_time', models.FloatField(blank=True, null=True)),
                ('dueDateClass', models.CharField(blank=True, max_length=25, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('event_type', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.category')),
                ('task_authorization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.taskauthorization')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
