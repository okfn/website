from django.conf.urls import url
# from django.contrib import admin

from . import views

urlpatterns = [
    url('contact/', views.contactview, name='contact'),
]
