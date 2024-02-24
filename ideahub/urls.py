from django.urls import path

from .views import dislike, ideas, like, set_collection_name, set_username

urlpatterns = [
    path("", set_collection_name, name="set_collection_name"),
    path(
        "like/<int:idea_id>/<int:user_id>",
        like,
        name="like",
    ),
    path(
        "dislike/<int:idea_id>/<int:user_id>",
        dislike,
        name="dislike",
    ),
    path("<str:collection_name>?name=<str:username>", ideas, name="ideas"),
    path("<str:collection_name>", set_username, name="set_username"),
]
