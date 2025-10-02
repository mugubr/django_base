from django.urls import path

from . import views

urlpatterns = [
    path("hello/", views.hello_api, name="hello-api"),
    path("users/", views.list_users, name="list-users"),
    path("users/create/", views.create_user, name="create-user"),
    path("posts/", views.list_posts, name="list-posts"),
    path("posts/create/", views.create_post, name="create-post"),
]
