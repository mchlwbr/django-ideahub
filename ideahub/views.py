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


def ideas(request, collection_name: str, username: str):
    collection, created = Collection.objects.get_or_create(name=collection_name.lower())
    user, created = User.objects.get_or_create(
        name=username.lower(), collection=collection
    )

    if request.method == "POST":
        idea_form = IdeaForm(request.POST)
        if idea_form.is_valid():
            idea: Idea = idea_form.save(commit=False)
            idea.user = user
            idea.collection = collection
            try:
                idea.save()
                # clear fields of idea_form
                idea_form = IdeaForm()
            except IntegrityError:
                idea_form.add_error(
                    "title",
                    f"Idea '{idea_form.cleaned_data['title']}' already exists in collection '{collection.name}'",
                )
            except Exception:
                pass
    else:
        idea_form = IdeaForm()

    ideas = collection.idea_set.all()
    sorted_ideas = sorted(ideas, key=lambda idea: idea.score, reverse=True)

    return render(
        request,
        "ideahub/ideas.html",
        {"user": user, "ideas": sorted_ideas, "idea_form": idea_form},
    )


def vote(request):
    if request.method == "POST":
        idea_id = request.POST.get("idea_id")
        idea = Idea.objects.get(pk=idea_id)

        user_id = request.POST.get("user_id")
        user = User.objects.get(pk=user_id)

        is_like_value = request.POST.get("is_like", "").lower()
        is_like = (
            True
            if is_like_value == "true"
            else False if is_like_value == "false" else None
        )

        vote, created = Vote.objects.get_or_create(user=user, idea=idea)
        if is_like == vote.is_like:
            vote.is_like = None
        else:
            vote.is_like = is_like

        vote.save()
        return redirect(
            "ideas", collection_name=user.collection.name, username=user.name
        )
