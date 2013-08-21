#import sys
#import site
#import os
#
#envpath = '/Library/python/2.7/site-packages'
#
## we add currently directory to path and change to it
#pwd = os.path.dirname(os.path.abspath(__file__))
#os.chdir(pwd)
#sys.path = [pwd] + sys.path
#
## Append paths
#site.addsitedir(envpath)
#
## now start django
#from django.core.handlers.wsgi import WSGIHandler
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#application = WSGIHandler()