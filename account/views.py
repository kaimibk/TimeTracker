from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from account.forms import SignUpForm, ProfileForm
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/accounts/login/')
# def redirect_unauth(request):
#     print("A THING")
#     render(request, "home_page.html")

def register_user(request):
    print("Here")
    if request.method == "POST":
        print("HERE2")
        user_form = UserCreationForm(request.POST)
        profile_form = SignUpForm(request.POST)

        print(user_form)
        print(profile_form)

        if user_form.is_valid() and profile_form.is_valid():
            print("HERE3")
            user = user_form.save()
            user.refresh_from_db()
            user.first_name = profile_form.cleaned_data.get("first_name")
            user.last_name = profile_form.cleaned_data.get("last_name")
            user.email = profile_form.cleaned_data.get("email")
            # user.employee_id = profile_form.cleaned_data.get("employee_id")
            user.pto_balance = profile_form.cleaned_data.get("pto_balance")

            user.profile.first_name = profile_form.cleaned_data.get("first_name")
            user.profile.last_name = profile_form.cleaned_data.get("last_name")
            user.profile.email = profile_form.cleaned_data.get("email")
            # user.profile.employee_id = profile_form.cleaned_data.get("employee_id")
            user.profile.pto_balance = profile_form.cleaned_data.get("pto_balance")

            group = Group.objects.get(name="Editors")
            user.groups.add(group)

            name_upper = user.username.upper()
            
            user.save()
            username = user_form.cleaned_data.get("username")
            raw_password = user_form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print("Redirecting")
            return redirect("/")

    else:
        user_form = UserCreationForm()
        profile_form = SignUpForm()
        
        return render(
            request, 
            "registration/register.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "path": request.path_info
            }
        )