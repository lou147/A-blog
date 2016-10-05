from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<slug>[\w-]+)/detail$', views.detail, name='detail'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^create', views.create, name='create'),
    url(r'^(?P<slug>[\w-]+)/edit', views.edit, name='edit'),
    url(r'^(?P<slug>[\w-]+)/detail/delete', views.delete),
    url(r'^registered', views.register, name='register'),
]
