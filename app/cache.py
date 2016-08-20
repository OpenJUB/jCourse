from django.template import loader, RequestContext
from django.http import HttpRequest
from app.context_processor import *


def create_timeline_cache():
    context = course_timeline_context()
    template = loader.get_template('objects/courses_timeline.html')
    timeline_html = template.render(RequestContext(HttpRequest(), context))

    cache = TimelineCache(cached_html=timeline_html)
    cache.save()


def delete_timeline_cache():
    old_cache = TimelineCache.objects.earliest('create_time')
    old_cache.delete()


def mark_timeline_cache():
    cache = TimelineCache.objects.latest('create_time')
    cache.should_change_mark = True
    cache.save()


def is_marked_timeline_cache():
    cache = TimelineCache.objects.latest('create_time')
    return cache.should_change_mark


def get_timeline_context():
    context = {}

    if not TimelineCache.objects.all().count():
        create_timeline_cache()

    cache = TimelineCache.objects.latest('create_time')
    timeline_html = cache.cached_html
    context["timeline"] = timeline_html

    return context
