from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'showall', views.show_all, name='showall'),
    url(r'fail', views.show_all, name='fail'),
    url(r'contact', views.contact, name='contact'),
    url(r'drop_size', views.drop_size, name='drop_size'),
    url(r'drop_success', views.drop_success, name='drop_success'),
    url(r'', views.index, name='index')
]