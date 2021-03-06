from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bandsteps_app.views.home', name="home"),
    url(r'^logout/$', 'bandsteps_app.views.logout_page', name='Logout'),
    url(r'^login/$', 'bandsteps_app.views.login_page',),
    url(r'^register/$', 'bandsteps_app.views.register', name = 'Register'),# just user form 
    url(r'^landing/$', 'bandsteps_app.views.landing', name='Instructor Home'), # just list of drills , link to review drills, link to make new drills...
    url(r'^new_drill/$', 'bandsteps_app.views.new_drill', name='Create Drill'),# form with upload field(need to check size)
    url(r'^review/$', 'bandsteps_app.views.review', name='Drill Review'),
    url(r'^api/$', 'bandsteps_app.views.dispatch', name='api'),
    url(r'^drill/(?P<drill_id>\d+)/$', 'bandsteps_app.views.drill', name='Drill'),
    url(r'^set_loc/$', 'bandsteps_app.views.set_loc'),
    url(r'^api/lists/$', 'bandsteps_app.views.lists'),
    url(r'^next_set/(?P<drill_id>\d+)/$', 'bandsteps_app.views.next_set'),
    url(r'^prev_set/(?P<drill_id>\d+)/$', 'bandsteps_app.views.prev_set'),

    #angular stuff
    url(r'^angular/$', 'bandsteps_app.views.angular'),

    #ember stuff
    url(r'^ember/$', 'bandsteps_app.views.ember'),

    #enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
#static files like images and javascript 
urlpatterns += staticfiles_urlpatterns()


