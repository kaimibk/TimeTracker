import sys
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from datetime import datetime, timedelta, date
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
import calendar
import holidays
from django.forms.models import model_to_dict
from account.models import Profile

# print weekday_count
def get_weekdays(year, month):
    cal = calendar.Calendar()
    return [x for x in cal.itermonthdays2(year, month) if x[0] !=0 and x[1] < 5]

def str_to_class(str):
    return getattr(sys.modules['home.models'], str)

def get_model_fields(model):
    fields = []
    options = model._meta
    for field in options.get_fields():
        fields.append(field.name)
    return fields

class CorporateHolidays(holidays.UnitedStates):
    # TODO: Expose via admin interface
    def _populate(self, year):
        # Populate the holiday list with the default US holidays
        holidays.UnitedStates._populate(self, year)
        # Remove Columbus Day
        self.pop_named("Columbus Day")
        # Add Ninja Turtle Day
        # self[date(year, 7, 13)] = "Ninja Turtle Day"

class HomePage(Page):
    description = RichTextField(null=True, blank=True)
    subheader = RichTextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('subheader'),
        FieldPanel('content'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # TODO: filter on payperiod / calendar month
        # TODO: context should inherit/relate to year/month/pay period objects.
        # TODO: Remove PTO from Display
        # TODO: Add BAH Metric, fix billable metric
        # TODO: Need to add G#'s to calendar drop downs
        
        today = datetime.now()

        activeTaskAuths = TaskAuthorization.objects.filter(end_date__gte=today)
        context["taskAuthorization"] = activeTaskAuths
        month_weekdays = get_weekdays(today.year, today.month)
        minimumHoursTotal = len(month_weekdays) * 8
        context["minimumHoursTotal"] = minimumHoursTotal
        # context["holidaysAll"] = CorporateHolidays(years=today.year)
        
        payPeriod = 0
        if today.day <= 15:
            payperiod_weekdays = [(i, j) for i,j in month_weekdays if i<= 15]
            payPeriod = 1 #First Half
        else:
            payperiod_weekdays = [(i, j) for i,j in month_weekdays if i > 15]
            payPeriod = 2 #Second Half
        
        minimumHoursPayPeriod = len(payperiod_weekdays) * 8
        context["minimumHoursPayPeriod"] = minimumHoursPayPeriod
        context["holidaysMonth"] = [i for i, j in CorporateHolidays(years=today.year).items() if i.month == today.month]
        
        events_month = Event.objects.filter(
            start__year=today.date().year,
            start__month=today.date().month
        )

        if payPeriod == 1:
            events_pp = Event.objects.filter(
                start__year=today.date().year,
                start__month=today.date().month, 
                start__day__lte=15,

            )
        else:
            events_pp = Event.objects.filter(
                start__year=today.date().year,
                start__month=today.date().month, 
                start__day__gt=15,

            )

        events_today = Event.objects.filter(
            start__year=today.date().year,
            start__month=today.date().month, 
            start__day=today.date().day
        )


        task_auth_today = {}
        task_auth_month = {}
        task_auth_pp = {}
        hours_today = 0
        hours_month = 0
        hours_pp = 0
        total_ta_allocated = 0
        total_ta_hours_spent = 0
        total_ta_spent_billable = 0
        
        for event in events_today:
            # task_auth_today.add(event.task_authorization)
            key = event.task_authorization.charge_code.name
            hours_today += event.delta_time

            if task_auth_today.get(key):
                task_auth_today[key] += event.delta_time
            else:
                task_auth_today[key] = event.delta_time

        for em in events_month:
            key = em.task_authorization.charge_code.name
            hours_month += em.delta_time

            if task_auth_month.get(key):
                task_auth_month[key] += em.delta_time
            else:
                task_auth_month[key] = em.delta_time

        for epp in events_pp:
            key = epp.task_authorization.charge_code.name
            hours_pp += epp.delta_time

            if task_auth_pp.get(key):
                task_auth_pp[key] += epp.delta_time
            else:
                task_auth_pp[key] = epp.delta_time

        for ta in activeTaskAuths:
            total_ta_allocated += ta.hours_allocated
            total_ta_hours_spent += ta.hours_spent

            if ta.is_billable == True:
                total_ta_spent_billable += ta.hours_spent

        # For every task in today, return the hours spent
        context["taskRecordToday"] = task_auth_today
        context["hoursSpentToday"] = hours_today #sum([i for i in task_auth_today.values()])

        context["taskRecordMonth"] = task_auth_month
        context["hoursSpentMonth"] = hours_month
        context["hoursRemainingMonth"] = minimumHoursTotal - hours_month

        context["hoursRemainingPayPeriod"] = minimumHoursPayPeriod - hours_pp
        context["projectedTaskAuth"] = round((total_ta_allocated / minimumHoursTotal)*100,2)
        if total_ta_allocated != 0:
            context["totalUtilTaskAuth"] = round((total_ta_hours_spent/total_ta_allocated)*100, 2)
        # _test = sum([float(task.hours_spent) for task in TaskAuthorization.objects.filter(end_date__gte=today)])
        # print(_test)

        return context

    def serve(self, request):
        print(request)
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/account/login/")
        else:
            # return render(request, "home/home_page.html", super().get_context(request))
            return super().serve(request)

class TablesPage(Page):
    dbModel = models.CharField(max_length=255, blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('dbModel'),
    ]
    

    def get_context(self, request):
        context = super().get_context(request)
        context["header"] = ''
        context["objs"] = ''
        some_list = []

        stc = str_to_class(str(self.dbModel))
        objs = stc.objects.filter(user=request.user.id)
        header = stc.objects.first()
        _header = model_to_dict(header)
        if 'user' in _header.keys():
            del _header['user']

        for obj in objs:
            _obj = model_to_dict(obj)
            if 'user' in _obj.keys():
                del _obj['user']
            some_list.append(_obj   )


        if header:
            context["header"] = _header
            context["objs"] = some_list
        context["model"] = self.dbModel
        return context


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

@register_snippet
class TaxLocation(models.Model):
    abbreviation = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    def __str__(self):
        return self.abbreviation
    
@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    
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