from django.conf.urls import url
from . import views
from Algo import Classify

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    #url(r'^$', views.upload, name='upload'),
    url(r'^_Matplotlib/Bar/$', Classify.GraphsViewBar),
    #url(r'^$', views.input, name='input')
]