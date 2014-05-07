import json

from django.template import Context, Template, loader, RequestContext
from django.http import  HttpRequest

from app.models import *
from app.course_info import *
from app.context_processor import *

def create_timeline_cache():
    context = course_timeline_context()
    template = loader.get_template('objects/courses_timeline.html')
    timeline_html = template.render(RequestContext(HttpRequest(),context))

    cache = HomeCache(cached_html=timeline_html)
    cache.save()

def delete_timeline_cache():
    old_cache = HomeCache.objects.earliest('create_time')
    old_cache.delete()

def get_timeline_context():
    context = {}

    cache = HomeCache.objects.latest('create_time')
    timeline_html = cache.cached_html
    context["timeline"] = timeline_html

    return context