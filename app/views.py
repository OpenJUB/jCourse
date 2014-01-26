
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    context = {
        "page": "home",
    }

    return render(request, "pages/home.html", context)