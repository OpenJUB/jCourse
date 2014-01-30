
# Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse

# Mimetypes for images
from mimetypes import guess_type

# App Models
from app.models import *
from app.course_info import *
from app.context_processor import *

def home(request):
    context = {
        "page": "home",
    }
    # Get courses
    courses = Course.objects.all()
    context = dict(context.items() + course_timeline_context(courses).items())

    return render(request, "pages/home.html", context)

def course_page(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        "page": "course"
    }
    context = dict(context.items() + course_page_context(course).items())

    return render(request, "pages/course.html", context)

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
        'page': 'all_comments'
    }
    context['comments'] = Comment.objects.all()

    return render(request, 'pages/comments.html', context)

def login_action(request):
    if request.method != 'POST':
        raise Http404

    if not 'url' in request.POST or not request.POST['url'] or \
        not 'login' in request.POST or not request.POST['login']
            raise Http404

    login_user = request.POST['user']
    login_pass = request.POST['pass']

    go('https://campusnet.jacobs-university.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-A9PnS7.Eby4LCWWmmtOcbYKUQ-so-sF48wtHtVNWX9aIeYmoSh5mej--SCbT.jubdlAouHy3dHzwyr-O.ufj3NVAYCNiJr0CFcBNwA3xADclRCTyqC0Oip8drT0F=')
    fv('1', 'usrname', username)
    fv('1', 'pass', password)
    submit('3')
    login_result = show()
    if login_result.find('Wrong username or password') != -1:
        pass
    else:
        juser = get_object_or_404(jUser)
        login = Login()

    return render(request, "objects/login.html", context)    
