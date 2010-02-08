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
    url(r'^$', 'djangovoice.views.list', name='djangovoice_home'),
    url(r'^(?P<list>all|open|closed|mine)/$', 'djangovoice.views.list', name='djangovoice_list'),
    url(r'^(?P<list>all|open|closed|mine)/(?P<type>[-\w]+)/$', 'djangovoice.views.list', name='djangovoice_list_type'),
    url(r'^(?P<list>all|open|closed|mine)/(?P<type>[-\w]+)/(?P<status>[-\w]+)/$', 'djangovoice.views.list', name='djangovoice_list_type_status'),
    url(r'^widget/$', 'djangovoice.views.widget', name='djangovoice_widget'),
    url(r'^submit/$', 'djangovoice.views.submit', name='djangovoice_submit'),
    url(r'^(?P<object_id>\d+)/$', 'djangovoice.views.detail', name='djangovoice_item'),
    url(r'^(?P<object_id>\d+)/edit/$', 'djangovoice.views.edit', name='djangovoice_edit'),
    url(r'^(?P<object_id>\d+)/delete/$', 'djangovoice.views.delete', name='djangovoice_delete'),
    url(r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)/?$', vote_on_object, feedback_dict, name='djangovoice_vote'),
)
