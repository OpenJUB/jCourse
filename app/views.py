
# Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse

# Mimetypes for images
from mimetypes import guess_type

# App Models
from app.models import *
from app.course_info import *

def home(request):
    context = {
        "page": "home",
    }
    categories = MAJOR_TYPES

    # Get courses
    courses = Course.objects.all()
    context['courses'] = []
    for course in courses:
        noSchoolCatalogue = course.catalogue \
            .replace('School of Humanities and Social Sciences', '') \
            .replace('School of Engineering and Science', '') \
            .replace('Language Courses', '')
        major = ""
        school = ""
        studies = "UG" if " Undergraduate Level Courses" in course.catalogue else ("Grad" if " Graduate Level Courses" in course.catalogue else "")
        for m in categories:
            if m[1] in noSchoolCatalogue:
                major = m[0]
                school = m[2]
        context['courses'].append({
            'course': course,
            'profs': course.instructors.all(),
            'major': major,
            'school': school,
            'studies': studies
        })
    context['categories'] = categories
    print categories

    return render(request, "pages/home.html", context)

def course_page(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        "page": "course"
    }
    context['course'] = course
    context['instructors'] = course.instructors.all()

    return render(request, "pages/course.html", context)

def get_course_image(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not course.image:
        raise Http404

    content_type = guess_type(course.image.name)
    return HttpResponse(course.image, mimetype=content_type)