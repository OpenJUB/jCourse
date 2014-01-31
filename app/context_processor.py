
from app.models import *
from app.course_info import *

def user_authenticated(request):
    if request.user and request.user.is_authenticated():
        return request.user.username
    return False

def course_timeline_context(courses):
    context = {}

    categories = MAJOR_TYPES

    courses = sorted(courses, key=lambda x: x.name)

    # Add the courses to the context
    context['courses'] = []
    for course in courses:
        noSchoolCatalogue = course.catalogue \
            .replace('School of Humanities and Social Sciences', 'SHSS') \
            .replace('School of Engineering and Science', 'SES') \
            .replace('Language Courses', 'Language') \
            .replace('Undergraduate Level Courses', 'UnderGrad') \
            .replace('Graduate Level Courses', 'Grad')

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
            'studies': studies,
            'catalogue': noSchoolCatalogue
        })
    context['categories'] = categories

    return context

def course_page_context(course):
    context = {}
    context['course'] = course

    course_types = dict(COURSE_TYPES)
    context['course_type'] = course_types[course.course_type]
    context['instructors'] = course.instructors.all()

    comments = Comment.objects.filter(course=course)
    context['comments'] = comments

    return context
