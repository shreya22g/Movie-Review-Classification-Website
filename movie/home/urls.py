from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path("",views.index,name="home"),
    path("home",views.index,name="home"),
    path("services",views.services,name="services"),
    path("review",views.review,name="review"),
    path("list",views.list,name="list"),
    path("view",views.view,name="view"),
]
