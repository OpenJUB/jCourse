from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^$', 'app.views.home'),
    url(r'^all_comments$', 'app.views.all_comments', name='all_comments'),
    url(r'^course/(?P<slug>[\w-]+)', 'app.views.course_page', name='course_page'),
    url(r'^course_image/(?P<slug>[\w-]+)', 'app.views.get_course_image', name='course_image'),
    url(r'^submit_comment', 'app.views.submit_comment', name='submit_comment'),
    url(r'^login','app.views.login_action', name='login'),
    url(r'^logout', 'app.views.logout_action', name='logout'),
    url(r'^vote_course', 'app.views.vote_course', name='vote_course'),

    url(r'^compare_course$', 'app.views.compare_start', name='compare_start'),
    url(r'^compare_course/(?P<slug1>[\w-]+)$', 'app.views.compare_next', name='course_next'),
    url(r'^compare_course/(?P<slug1>[\w-]+)/(?P<slug2>[\w-]+)$', 'app.views.compare', name='compare'),
)