import json

from app.models import *
from app.course_info import *
from app.ratings import *

def user_authenticated(request):
    if request.user and request.user.is_authenticated():
        return request.user.username
    return False

def course_timeline_context():
    context = {}

    categories = MAJOR_TYPES

    courses = Course.objects.all()
    courses = sorted(courses, key=lambda x: x.name)

    # Add the courses to the context
    allcourses = []
    for course in courses:
        noSchoolCatalogue = course.catalogue \
            .replace('School of Humanities and Social Sciences', 'SHSS') \
            .replace('School of Engineering and Science', 'SES') \
            .replace('Language Courses', 'Language') \
            .replace('Undergraduate Level Courses', 'UnderGrad') \
            .replace('Graduate Level Courses', 'Grad')

        major = ""
        school = ""
        term = ""
        studies = "UG" if " Undergraduate Level Courses" in course.catalogue else ("Grad" if " Graduate Level Courses" in course.catalogue else "")
        
        ratings = Rating.objects.filter(course= course, rating_type=OVERALL_R)
        if (len(ratings) == 0):
            overall_rating = None
        else:   
            overall_rating = sum([cur.rating for cur in ratings])/len(ratings)

        for m in categories:
            if m[1] in noSchoolCatalogue:
                major = m[0]
                school = m[2]
        for t in TERM_TYPES:
            if t in course.catalogue:
                term = t
        allcourses.append({
            'course': course,
            'profs': course.instructors.all(),
            'major': major,
            'school': school,
            'term': term,
            'studies': studies,
            'catalogue': noSchoolCatalogue,
            'overall_rating': overall_rating
        })
    allcourses = sorted(allcourses, key=lambda x:x['overall_rating'], reverse=True)
    context['courses'] = allcourses

    context['categories'] = categories

    return context

def comment_context(comment, request, current_user):
    context_comment = {
        'comment': comment
    }
    details = CommentDetails.objects.get_or_create(comment=comment)[0]

    upvotes = details.upvoted_by.all().count()
    downvotes = details.downvoted_by.all().count()
    context_comment['rating'] = comment_rating(upvotes+1, downvotes)
    if upvotes + downvotes > 0:
        context_comment['score'] = str(upvotes) + "/" + str(upvotes + downvotes)

    already_voted = False
    if current_user:
        users_votes = CommentDetails.objects.filter(comment=comment, upvoted_by=current_user) | \
            CommentDetails.objects.filter(comment=comment, downvoted_by=current_user)
        if users_votes:
            already_voted = True

    shouldnt_vote = False
    if details.posted_by:
        context_comment['posted_by'] = details.posted_by
        if current_user:
            if details.posted_by == current_user:
                shouldnt_vote = True

    context_comment['should_vote'] = not already_voted and not shouldnt_vote

    return context_comment


def course_page_context(request, course):
    context = {}
    context['course'] = course

    course_types = dict(COURSE_TYPES)
    context['course_type'] = course_types[course.course_type]
    context['instructors'] = course.instructors.all()

    context['ratings'] = []
    allratings = Rating.objects.filter(course= course)
    for rating_type in RATING_TYPES:
        ratings = allratings.filter(rating_type=rating_type[0])
        if len(ratings) > 0:
            rating = sum([cur.rating for cur in ratings])/len(ratings)
        else:
            rating = None
        context_rating = {
            'type': rating_type[1],
            'type_db': rating_type[0],
        }
        specific_rating = {
            'score': rating,
            'count': len(ratings)
        }
        if request.user.is_authenticated():
            users = jUser.objects.filter(id=request.user.id)
            if len(users) > 0:
                user = users[0]
                my_ratings = ratings.filter(user=user)
                if len(my_ratings) > 0:
                    specific_rating['my_score'] = my_ratings[0].rating
        if rating_type[1] != 'Professor':
            context['ratings'].append( dict(context_rating.items() + specific_rating.items()) )
        else:
            professors = course.instructors.all()
            for prof in professors:
                profratings = Professor_Rating.objects.filter(course= course, prof=prof)
                if len(profratings) > 0:
                    profrating = sum([cur.rating for cur in profratings])/len(profratings)
                else:
                    profrating = None
                specific_rating = {
                    'score': profrating,
                    'count': len(profratings),
                    'prof': prof.name
                }
                if request.user.is_authenticated():
                    users = jUser.objects.filter(id=request.user.id)
                    if len(users) > 0:
                        user = users[0]
                        my_ratings = profratings.filter(user=user)
                        if len(my_ratings) > 0:
                            specific_rating['my_score'] = my_ratings[0].rating
                context['ratings'].append( dict(context_rating.items() + specific_rating.items()) )


    current_user = None
    if request.user.is_authenticated():
        current_user = jUser.objects.get(id=request.user.id)

    comments = Comment.objects.filter(course=course)
    context['comments'] = []
    for comment in comments:
        context['comments'].append( comment_context(comment, request, current_user) )


    return context
