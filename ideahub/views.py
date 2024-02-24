from django.db.utils import IntegrityError
from django.shortcuts import redirect, render

from .forms import CollectionForm, IdeaForm, UserForm
from .models import Collection, Idea, User, Vote


def set_collection_name(request):
    if request.method == "POST":
        collection_form = CollectionForm(request.POST)
        if collection_form.is_valid():
            collection = collection_form.save()
            return redirect("set_username", collection_name=collection.name)
    else:
        collection_form = CollectionForm()
    return render(
        request,
        "ideahub/set_collection_name.html",
        {"collection_form": collection_form},
    )


def set_username(request, collection_name: str):
    if username := request.GET.get("name"):
        return redirect("ideas", collection_name=collection_name, username=username)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            collection, created = Collection.objects.get_or_create(
                name=collection_name.lower()
            )
            username = user_form.cleaned_data["name"]
            user, created = User.objects.get_or_create(
                name=username.lower(), collection=collection
            )
            return redirect(
                "ideas", collection_name=collection.name, username=user.name
            )
    else:
        user_form = UserForm()
    return render(
        request,
        "ideahub/set_user.html",
        {"collection_name": collection_name, "user_form": user_form},
    )


def ideas(request, collection_name: str, username: str, idea_form=None):
    collection, created = Collection.objects.get_or_create(name=collection_name.lower())
    user, created = User.objects.get_or_create(
        name=username.lower(), collection=collection
    )
    idea_form = idea_form or IdeaForm()

    sorted_ideas = collection.idea_set.all().order_by("-score")

    return render(
        request,
        "ideahub/ideas.html",
        {"user": user, "ideas": sorted_ideas, "idea_form": idea_form},
    )


def submit_idea(request, user_id: int):
    user = User.objects.get(pk=user_id)
    idea_form = IdeaForm(request.POST)
    if idea_form.is_valid():
        idea: Idea = idea_form.save(commit=False)
        idea.user = user
        idea.collection = user.collection
        try:
            idea.save()
            # clear fields of idea_form
            idea_form = IdeaForm()
        except IntegrityError:
            idea_form.add_error(
                "title",
                f"Idea '{idea_form.cleaned_data['title']}' already exists in collection '{user.collection.name}'",
            )
    else:
        return redirect(
            "ideas", collection_name=user.collection.name, username=user.name
        )

    return ideas(
        request=request,
        collection_name=user.collection.name,
        username=user.name,
        idea_form=idea_form,
    )


def like(request, idea_id: int, user_id: int):
    return vote(request, idea_id, user_id, True)


def dislike(request, idea_id: int, user_id: int):
    return vote(request, idea_id, user_id, False)


def vote(request, idea_id: int, user_id: int, is_like: bool):
    idea = Idea.objects.get(pk=idea_id)
    user = User.objects.get(pk=user_id)

    vote, created = Vote.objects.get_or_create(user=user, idea=idea)
    if is_like == vote.is_like:
        vote.delete()
    else:
        vote.is_like = is_like
        vote.save()

    # fetch idea with updated score
    idea = Idea.objects.get(pk=idea_id)
    return render(request, "ideahub/idea.html", {"idea": idea, "user": user})
