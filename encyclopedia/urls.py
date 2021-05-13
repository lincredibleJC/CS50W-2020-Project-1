from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("wiki/<str:title>", views.wiki, name="wiki"),
	path("wiki/<str:title>/edit", views.edit_entry, name="edit_entry"),
	path("wiki/", views.random_entry, name="random_entry"),
	path("search", views.search_entry, name="search_entry"),
	path("create_entry", views.create_entry, name="create_entry"),

]
