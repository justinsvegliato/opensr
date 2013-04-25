from django.conf.urls import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('portal.urls')),
    url(r'^password_required/$', 'password_required.views.login'),    
)