from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/(?P<cate>\w+)', views.categories_detail, name='categories_detail'),
]
