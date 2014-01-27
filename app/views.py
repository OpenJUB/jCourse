
from django.shortcuts import render, redirect, get_object_or_404

from app.models import *

def home(request):
    context = {
        "page": "home",
    }

    # Get courses
    courses = Course.objects.all()
    context['courses'] = []
    for course in courses:
        context['courses'].append({
            'course': course,
            'profs': course.instructors.all()
        })

    return render(request, "pages/home.html", context)