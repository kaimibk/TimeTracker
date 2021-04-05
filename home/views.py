from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse
from home.models import HomePage
from event.models import Event
from chargecode.models import ChargeCode
from category.models import Category
from taskauthorization.models import TaskAuthorization
import requests
from datetime import datetime
from django.utils import timezone
from django.shortcuts import redirect
from django.forms.models import model_to_dict
import json

try:
    PARENT_PAGE = HomePage.objects.all().first()
except:
    pass

def get_chargecodes(request):
    render_tasks = TaskAuthorization.objects.all()

    response = []
    
    for task in render_tasks:
        cc = task.charge_code

        response.append(
            {
                "id": str(cc.id),
                "name": cc.name,
                "color": cc.color,
                "bgColor": cc.bgColor,
                "dragBgColor": cc.dragBgColor,
                "borderColor": cc.borderColor,
            }
        )
    
    return JsonResponse({"response": response})

def get_events(request):
    renderStart = json.loads(request.GET.get("renderStart")).get("_date").replace("Z", "")
    renderEnd = json.loads(request.GET.get("renderEnd")).get("_date").replace("Z", "")
    user = request.user
    
    print(f"Retrieve Events ({user}): [{renderStart}, {renderEnd}]")

    render_events = Event.objects.filter(start__gte=renderStart, end__lte=renderEnd, user=user)

    response = []
    
    for event in render_events:
        response.append(
            {
                "id": event.id,
                "calendarId": event.task_authorization.charge_code.id,
                "title": event.title,
                "isAllDay": event.isAllDay,
                "start": event.start.isoformat(),
                "end": event.end.isoformat(),
                "category": event.category.name,
                "dueDateClass": event.dueDateClass,
                "location": event.location,
                "event_type": event.event_type,
                "notes": event.notes
            }
        )
    
    return JsonResponse({"response": response})

def add_event(request):
    # TODO: Modify to store timezone
    _event = json.loads(request.GET.get("event"))
    category, created = Category.objects.get_or_create(name=_event.get("category"))
    print(_event["calendarId"])
    task_authorization = TaskAuthorization.objects.get(charge_code=_event["calendarId"])
    temp = {
        "id":_event["id"],
        "title": _event["title"],
        "isAllDay":_event["isAllDay"],
        "start": datetime.fromisoformat(_event["start"]["_date"].replace("Z", "")),
        "end": datetime.fromisoformat(_event["end"]["_date"].replace("Z", "")),
        "category":category,
        "dueDateClass": _event["dueDateClass"],
        # "task_authorization": task_authorization,
        # "charge_code": _event[""],
        # "location":_event["location"],
        # "notes": _event[""],
    }

    temp["delta_time"] = (temp["end"] - temp["start"]).total_seconds() / 60 / 60.

    task_authorization.hours_spent += temp["delta_time"]
    task_authorization.hours_remaining -= temp["delta_time"]
    task_authorization.hours_percentage = (task_authorization.hours_spent / task_authorization.hours_allocated) * 100.0

    temp["task_authorization"] = task_authorization

    task_authorization.save()

    if request.user.is_authenticated:
        temp["user"] = request.user
    
    event = Event(**temp)

    print(f"Create Event ({request.user}): {_event['id']}")
    event.save()

    return JsonResponse({"response": "Recieved"})

def remove_event(request):
    _event = json.loads(request.GET.get("event"))
    event = Event.objects.get(id=_event)

    task_authorization = event.task_authorization

    task_authorization.hours_spent -= event.delta_time
    task_authorization.hours_remaining += event.delta_time
    task_authorization.hours_percentage = (task_authorization.hours_spent / task_authorization.hours_allocated) * 100.0

    task_authorization.save()

    print(f"Delete Event ({request.user}): {event}")
    event.delete()

    return JsonResponse({"response": "success"})

def update_event(request):
    _event = json.loads(request.GET.get("event"))
    _changes = json.loads(request.GET.get("changes"))

    event = Event.objects.get(id=_event)
    
    _delta_time = event.delta_time
    # task_authorization = event.task_authorization

    for change in _changes:
        if change == "end":
            event.end = datetime.fromisoformat(_changes[change]["_date"].replace("Z", ""))
        elif change == "start":
            event.start = datetime.fromisoformat(_changes[change]["_date"].replace("Z", ""))
        elif change == "title":
            event.title = _changes[change]
        elif change == "calendarId":
            event.charge_code = ChargeCode.objects.get(id=_changes[change])

    if ("end" in _changes) or ("start" in _changes):
        # TODO: Update allow for timezone
        start = event.start.replace(tzinfo=None)
        # TODO: Allow for timezone
        end = event.end.replace(tzinfo=None)
        print(start, end)
        event.delta_time = (end - start).total_seconds() / 60 / 60

        task_authorization = event.task_authorization

        task_authorization.hours_spent -= _delta_time
        task_authorization.hours_spent += event.delta_time
        
        task_authorization.hours_remaining += _delta_time
        task_authorization.hours_remaining -= event.delta_time

        task_authorization.hours_percentage = (task_authorization.hours_spent / task_authorization.hours_allocated) * 100.0

        task_authorization.save()

        # TODO: Add remaining change conditionals

    print(f"Update Event ({request.user}): {event} \t Attributes: {_changes.keys()}")
    event.save()

    return JsonResponse({"response": "success"})

def create_taskauth(request):

    idx = request.POST.get("id_taskauthorization")

    params = {
        "user": request.user,
        "hours_allocated": float(request.POST.get("ta_hours_allocated")),
        "hours_spent": float(request.POST.get("ta_hours_spent")),
        "start_date": request.POST.get("ta_start_date"),
        "end_date": request.POST.get("ta_end_date"),
        #"tax_code": request.POST.get("ta_tax_code"),
        "ta_file": request.POST.get("ta_file"),
    }

    params["hours_remaining"] = params["hours_allocated"] - params["hours_spent"]
    params["hours_percentage"] = (params["hours_spent"] / params["hours_allocated"])*100.0

    exists = TaskAuthorization.objects.filter(id=idx).exists()

    if not exists:
        task_authorization = TaskAuthorization(**params)

    else:
        task_authorization = TaskAuthorization.objects.get(id=idx)

        task_authorization.hours_allocated = params["hours_allocated"]
        task_authorization.hours_spent = params["hours_spent"]
        task_authorization.hours_remaining = params["hours_remaining"]
        task_authorization.hours_percentage = params["hours_percentage"]
        task_authorization.start_date = params["start_date"]
        task_authorization.end_date = params["end_date"]
        # task_authorization.tax_code = params["tax_code"]
        task_authorization.ta_file = params["ta_file"]

    task_authorization.save()

    print("Save Task Authorization")
    print(task_authorization)
    
    return redirect(PARENT_PAGE.url)


def create_chargecode(request):
    
    idx = request.POST.get("id_chargecode")
    
    params = {
        "name": request.POST.get("name"),
        "code": request.POST.get("code"),
        "color": request.POST.get("color"),
        # TODO: Add remaining colors
        "personal_list": bool(request.POST.get("personal_list")),
    }
        
    exists = ChargeCode.objects.filter(id=idx).exists()
    
    if not exists:
        charge_code = ChargeCode(**params)

    else:
        charge_code = ChargeCode.objects.get(id=idx)
        charge_code.name = params["name"]
        charge_code.code = params["code"]
        charge_code.personal_list = params["personal_list"]
        charge_code.color = params["color"]

    charge_code.save()
    
    print("Save Charge")
    print(charge_code)
    
    return redirect(PARENT_PAGE.url)
    # return JsonResponse({"response" : params})


def get_chargecode(request):
    idx = request.GET.get("id_code")
    charge_code = ChargeCode.objects.get(id=idx)
    _temp = model_to_dict(charge_code)
    _temp["ta_file"] = _temp["ta_file"].name
    return JsonResponse({"response" : _temp})

# def edit_chargecode(request):
#     idx = request.GET.get("id_code")
#     charge_code = ChargeCode.objects.get(id=idx)
    
#     return JsonResponse({"response" : model_to_dict(charge_code)})

def delete_chargecode(request):
    idx = request.GET.get("id_code")
    charge_code = ChargeCode.objects.get(id=idx)

    charge_code.delete()
    
    return redirect(PARENT_PAGE.url)

def get_taskauth(request):
    idx = request.GET.get("id_code")
    task_authorization = TaskAuthorization.objects.get(id=idx)
    _temp = model_to_dict(task_authorization)
    _temp["ta_file"] = _temp["ta_file"].name
    return JsonResponse({"response" : _temp})

# def edit_taskauth(request):
#     idx = request.GET.get("id_code")
#     task_authorization = TaskAuthorization.objects.get(id=idx)
    
#     return JsonResponse({"response" : model_to_dict(task_authorization)})

def delete_taskauth(request):
    idx = request.GET.get("id_code")
    task_authorization = TaskAuthorization.objects.get(id=idx)

    task_authorization.delete()
    
    return redirect(PARENT_PAGE.url)

def get_tables(request):
    return HttpResponse()