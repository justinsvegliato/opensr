from django.conf.urls import *

urlpatterns = patterns('portal.views',
    url(r'^(?P<test_id>\d)/$', 'index', name='index'),
    url(r'^test-selection/$', 'test_selection', name='test_selection'),
    url(r'^informed-consent/$', 'informed_consent', name='informed_consent'),
    url(r'^introduction/$', 'introduction', name='introduction'),
    url(r'^group/$', 'group', name='group'),
    url(r'^test/$', 'test', name='test'),
    url(r'^confirmation/$', 'confirmation', name='confirmation'),
    url(r'^record/$', 'record', name='record'),
)