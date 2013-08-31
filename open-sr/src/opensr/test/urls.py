from django.conf.urls import *

urlpatterns = patterns('portal.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<test_id>\d)/$', 'entrance', name='entrance'),
    url(r'^informed-consent/$', 'informed_consent', name='informed_consent'),
    url(r'^introduction/$', 'introduction', name='introduction'),
    url(r'^group/$', 'group', name='group'),
    url(r'^test/$', 'test', name='test'),
    url(r'^confirmation/$', 'confirmation', name='confirmation'),
    url(r'^record/$', 'record', name='record'),
)