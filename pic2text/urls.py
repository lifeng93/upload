"""upload URL Configuration"""

from django.conf.urls import url
from . import views

urlpatterns = [  
	url(r'^$', views.upload, name='upload'),
	url(r'^return_text/$', views.return_text, name='return_text'),
]
app_name = 'pic2text'