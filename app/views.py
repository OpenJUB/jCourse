
# Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Mimetypes for images
from mimetypes import guess_type

# App Models
from app.models import *
from app.course_info import *
from app.context_processor import *

from twill import commands

import os
import sys

def home(request):
    context = {
        "page": "home",
        'user_auth': user_authenticated(request)
    }
    # Get courses
    courses = Course.objects.all()
    context = dict(context.items() + course_timeline_context(courses).items())

    return render(request, "pages/home.html", context)

def course_page(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        "page": "course",
        'user_auth': user_authenticated(request)
    }
    context = dict(context.items() + course_page_context(request, course).items())

    return render(request, "pages/course.html", context)

@login_required
def vote_course(request):
    context = {}
    if request.method != 'POST':
        raise Http404
    user = get_object_or_404(jUser, id=request.user.id)

    if not 'course_id' in request.POST or not request.POST['course_id'] or \
        not 'rating_value' in request.POST or not request.POST['rating_value'] or \
        not 'rating_type' in request.POST or not request.POST['rating_type'] or \
        not 'url' in request.POST or not request.POST['url']:
            raise Http404        

    user = get_object_or_404(jUser, username= request.POST['username'])
    course = get_object_or_404(Course, id= request.POST['course_id'])
    rating_value = float(request.POST['rating_value'])
    rating_type = request.POST['rating_type']

    if not rating_type in dict(RATING_TYPES):
        raise Http404

    if rating_type != PROFESSOR_R:
        ratings = Rating.objects.filter(user= user, course= course, rating_type= rating_type)
        if len(ratings) == 0:
            rating = Rating(user= user, course= course, rating= rating_value, rating_type= rating_type)
            rating.save()
        else:
            rating = ratings[0]
            rating.rating = rating_value
            rating.save()
    else:
        if not 'profname' in request.POST or not request.POST['profname']:
            raise Http404
        prof = get_object_or_404(Professor, name=request.POST['profname'])
        ratings = Professor_Rating.objects.filter(user= user, course= course, rating_type= rating_type, prof=prof)
        if len(ratings) == 0:
            rating = Professor_Rating(user= user, course= course, rating= rating_value, rating_type= rating_type, prof=prof)
            rating.save()
        else:
            rating = ratings[0]
            rating.rating = rating_value
            rating.save()

    return redirect(request.POST['url'])


def get_course_image(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not course.image:
        raise Http404

    content_type = guess_type(course.image.name)
    return HttpResponse(course.image, mimetype=content_type)

def submit_comment(request):
    if request.method != 'POST':
        raise Http404

    if not 'url' in request.POST or not request.POST['url'] or \
        not 'comment' in request.POST or not request.POST['comment'] or \
        not 'course_id' in request.POST or not request.POST['course_id']:
            raise Http404

    course = get_object_or_404(Course, id= request.POST['course_id'])
    comment_text = request.POST['comment']
    comment = Comment(course= course, comment= comment_text)
    comment.save()

    return redirect(request.POST['url'])

def all_comments(request):
    context = {
        'page': 'all_comments',
        'user_auth': user_authenticated(request)
    }
    context['comments'] = Comment.objects.all()

    return render(request, 'pages/comments.html', context)

##### User authentication here on

def login_action(request):
    context = {}
    if request.method != 'POST':
        raise Http404

    if not 'user' in request.POST or not request.POST['user'] or \
        not 'pass' in request.POST or not request.POST['pass'] or \
        not 'url' in request.POST or not request.POST['url']:
            raise Http404

    login_user = request.POST['user']
    login_pass = request.POST['pass']

    commands.go('https://campusnet.jacobs-university.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-A9PnS7.Eby4LCWWmmtOcbYKUQ-so-sF48wtHtVNWX9aIeYmoSh5mej--SCbT.jubdlAouHy3dHzwyr-O.ufj3NVAYCNiJr0CFcBNwA3xADclRCTyqC0Oip8drT0F=')
    commands.fv('1', 'usrname', login_user)
    commands.fv('1', 'pass', login_pass)
    commands.submit('3')

    out = sys.stdout
    bin = open(os.devnull, 'w')
    sys.stdout = bin
    login_result = commands.show()
    sys.stdout = out

    if login_result.find('Wrong username or password') != -1:
        context['error'] = "Wrong username or password!"
        return render(request, "pages/login_page.html", context)
    
    users = jUser.objects.filter(username=login_user)
    if len(users) == 0:
        user = jUser.objects.create_user(username=login_user, password="1234")
        user.save()

    user = authenticate(username=login_user, password="1234")
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
            # return redirect(request.POST['url'])
        else:
            context['error'] = "Invalid user! Please try again! The account may not be activated!"
            return render(request, "pages/login_page.html", context)
    else:
        context['error'] = "Invalid login! Please try again!"
        return render(request, "pages/login_page.html", context)

    raise Http404

@login_required
def logout_action(request):
    if request.user:
        user = request.user
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('/')
