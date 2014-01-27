
# Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse

# Mimetypes for images
from mimetypes import guess_type

# App Models
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

def course_page(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not course.image:
        raise Http404

    raise Http404

def get_course_image(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not course.image:
        raise Http404

    content_type = guess_type(course.image.name)
    return HttpResponse(course.image, mimetype=content_type)