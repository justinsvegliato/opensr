from django.conf.urls import *

urlpatterns = patterns('portal.views',
    url(r'^agreement/$', 'agreement', name='agreement'),
    url(r'^group/$', 'group', name='group'),
    url(r'^test/$', 'test', name='test'),
    url(r'^survey/$', 'survey', name='survey'),
    url(r'^confirmation/$', 'confirmation', name='confirmation'), 
    url(r'^record/$', 'record', name='record'), 
)