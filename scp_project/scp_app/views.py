from django.shortcuts import render, redirect, HttpResponse
from .models import User, Event
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    request.session.flush()
    return render(request, "index.html")

def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(User.objects.filter(email=request.POST["email"])) > 0:
        errors["email_exists"] = "Email already exists"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":

            pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

            User.objects.create(
                username = request.POST["username"],
                email = request.POST["email"],
                password = pw_hash,
            )
            request.session["id"] = User.objects.last().id
            context = {
                "current_user": User.objects.last(),
                "all_events": Event.objects.all(),
            }
        return render(request, "login.html", context)

def login(request):
    if request.method == "GET":
        return redirect("/")
    else:
        errors = User.objects.email_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            if request.method == "POST":
                user = User.objects.filter(email=request.POST["email"])
                if user:
                    logged_user = user[0]
                    if bcrypt.checkpw(request.POST["password"].encode(), logged_user.password.encode()):
                        request.session["id"] = logged_user.id
                        context = {
                            "current_user": User.objects.get(id=request.session["id"]),
                            "all_events": Event.objects.all(),
                        }
                        return render(request, "index.html", context)
                    else:
                        messages.error(request, "Wrong Password")
                return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")
