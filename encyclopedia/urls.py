from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("wiki/", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage")
]
