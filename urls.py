from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from voting.views import vote_on_object
from djangovoice.models import Feedback


feedback_dict = {
    'model': Feedback,
    'template_object_name': 'feedback',
}


urlpatterns = patterns('',
    url(r'^$', 'djangovoice.views.list', name="djangovoice_home"),
    (r'^(?P<list>all|open|closed|mine)/$', 'djangovoice.views.list'),
    url(r'^(?P<list>all|open|closed|mine)/(?P<type>[-\w]+)/$', 'djangovoice.views.list', name='list_type'),
    url(r'^(?P<list>all|open|closed|mine)/(?P<type>[-\w]+)/(?P<status>[-\w]+)/$', 'djangovoice.views.list', name='list_type_status'),
    #(r'^open/$', 'djangovoice.views.open'),
    #(r'^closed/$', 'djangovoice.views.closed'),
    #(r'^mine/$', 'djangovoice.views.mine'),
    (r'^widget/$', 'djangovoice.views.widget'),
    (r'^submit/$', 'djangovoice.views.submit'),
    (r'^(?P<object_id>\d+)/$', 'djangovoice.views.detail'),
    (r'^(?P<object_id>\d+)/edit/$', 'djangovoice.views.edit'),
    (r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)/?$',    vote_on_object, feedback_dict),
)
