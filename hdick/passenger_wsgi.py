"""
WSGI config for hdick project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os,sys,site
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

site.addsitedir('/home/drhans666/site-packages') # glowny site-packages bazujac na module site
sys.path.insert(0,os.getcwd()) #kat z aplikacja
sys.path.insert(0,os.path.join(os.getcwd(), '/site-packages')) #kat site-packages w kat z aplikacja
#site.addsitedir(os.path.join(os.getcwd(), '/site-packages') #ew. to co wyzej ale przez site
#(jesli instalowales tam przez easy_install)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hdick.settings")
from django.core.wsgi import get_wsgi_application

#uruchomienie z wyswietlaniem bledow dla python 3.3
#import ErrorMiddlewareV
#application = ErrorMiddlewareV.EMV(get_wsgi_application(), True)

#uruchomienie z wyswietlaniem bledow dla python 2.7 i 2.6
#from paste.exceptions.errormiddleware import ErrorMiddleware
#application = get_wsgi_application()
#application = ErrorMiddleware(application, debug=True)

#uruchomienie bez wyswietlania bledow
application = get_wsgi_application()
