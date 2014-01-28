
# Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse

# Mimetypes for images
from mimetypes import guess_type

# App Models
from app.models import *
categories = ['Electrical Engineering and Computer Science', 'Life Sciences', 
'Logistics', 'Mathematical Sciences', 'Natural and Environmental Sciences', 
'Economics and Management', 'History', 'Humanities', 'Law', 'Psychology', 
'Social Sciences', 'Statistics and Methods', 'University Studies Courses', 
'German', 'French', 'Chinese', 'Spanish', 'Foundation Year']

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
    context['categories'] = categories

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