from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import ContactForm, LoginForm

def home_page(request):
    content = {
        "title": "Hello world",
        "content": "Welcome to the home page."
    }
    return render(request, "home_page.html", content)


def contact_page(request):
    form = ContactForm(request.POST or None)

    content = {
        "title": "Contact Page",
        "content": "Welcome to the Contact Page",
        "form": form,
    }

    if form.is_valid():
        print(form.cleaned_data)

    return render(request, "contact/views.html", content)


def login_page(request):
    form = LoginForm(request or None)
    content = {
        "form": form,
    }

    print(request.user.is_authenticated())

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            print("Login Error")

    return render(request, "auth/login.html", content)


def register_page(request):
    return render(request, "auth/register.html", {})


def about_page(request):
    return render(request, "about.html", {})














