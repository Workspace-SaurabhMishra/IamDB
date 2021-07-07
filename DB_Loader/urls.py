from django.urls import path
from . import views

urlpatterns = [
    path('default',views.def_loader)
]