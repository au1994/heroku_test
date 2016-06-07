from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^search/', views.search_movie, name='search_movie'),
        url(r'^exact/', views.exact_movie, name='exact_movie'),
        ]
