from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('sample', views.sample),
    path('signin', obtain_auth_token),
    path('signup', views.signup),
    path('search', views.search),
    path('update', views.update),
    path('delete', views.delete),
    path('signout', views.signout),
    path('fetch_all', views.fetch_all)
]
