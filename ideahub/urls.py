from django.urls import path

from .views import ideas, set_collection_name, set_username, vote

urlpatterns = [
    path("", set_collection_name, name="set_collection_name"),
    path("vote", vote, name="vote"),
    path("<str:collection_name>?name=<str:username>", ideas, name="ideas"),
    path("<str:collection_name>", set_username, name="set_username"),
]
