import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from ideahub.models import Collection, Idea, User, Vote

collection_name = "my_collection"
username = "my_user"


@pytest.mark.django_db
class Test_set_collection_name:
    def test_empty_db(self, client):
        url = reverse("set_collection_name")
        response = client.get(url)

        for model in [User, Collection, Idea, Vote]:
            assert model.objects.count() == 0

    def test_create_collection_via_post(self, client):
        url = reverse("set_collection_name")
        response = client.post(url, {"name": collection_name})

        assert Collection.objects.get(name=collection_name)

    def test_created_user_autofocus(self, client):
        url = reverse("set_collection_name")
        response = client.get(url)
        autofocus = (
            '<input type="text" name="name" maxlength="255" autofocus="autofocus"'
        )

        assert autofocus in str(response.content)


@pytest.mark.django_db
class Test_set_username:
    def test_dont_create_collection_via_get(self, client):
        url = reverse("set_username", kwargs={"collection_name": collection_name})
        response = client.get(url)

        assert Collection.objects.count() == 0

    def test_create_user_via_post(self, client):
        url = reverse(
            "set_username",
            kwargs={"collection_name": collection_name},
        )
        response = client.post(url, {"name": username})

        assert User.objects.count() == 1
        assert User.objects.get(name=username)

    def test_created_collection_is_lowercase(self, client):
        collection_name_uppercase = collection_name.upper()
        url = reverse(
            "set_username",
            kwargs={"collection_name": collection_name_uppercase},
        )
        response = client.post(url, {"name": username})

        assert Collection.objects.get(name=collection_name)
        with pytest.raises(ObjectDoesNotExist) as exx:
            Collection.objects.get(name=collection_name_uppercase)

    def test_same_collection_name_doesnt_create_new_collection(self, client):
        for name in [
            collection_name,
            collection_name.upper(),
            collection_name.capitalize(),
        ]:
            url = reverse(
                "set_username",
                kwargs={"collection_name": name},
            )
            response = client.post(url, {"name": username})

        assert Collection.objects.count() == 1
        assert Collection.objects.get(name=collection_name)

    def test_created_user_autofocus(self, client):
        url = reverse(
            "set_username",
            kwargs={"collection_name": collection_name},
        )
        response = client.get(url)
        autofocus = (
            '<input type="text" name="name" maxlength="255" autofocus="autofocus"'
        )

        assert autofocus in str(response.content)


@pytest.mark.django_db
class Test_ideas:
    def test_created_user_via_get(self, client):
        url = reverse(
            "ideas",
            kwargs={"collection_name": collection_name, "username": username},
        )
        response = client.get(url)

        assert User.objects.count() == 1
        assert User.objects.get(name=username)

    def test_created_collection_via_get_with_username(self, client):
        url = reverse(
            "ideas",
            kwargs={"collection_name": collection_name, "username": username},
        )
        response = client.get(url)

        assert Collection.objects.get(name=collection_name)

    def test_created_idea_via_post(self, client):
        url = reverse(
            "ideas",
            kwargs={"collection_name": collection_name, "username": username},
        )
        data = {"title": "my_ideas_title", "description": "my_ideas_description"}
        response = client.post(url, data)

        assert Idea.objects.count() == 1

    def test_created_idea_autofocus(self, client):
        url = reverse(
            "ideas",
            kwargs={"collection_name": collection_name, "username": username},
        )
        response = client.get(url)
        autofocus = (
            '<input type="text" name="title" maxlength="255" autofocus="autofocus"'
        )

        assert autofocus in str(response.content)


@pytest.mark.django_db
class Test_vote:
    def setup_method(self, client):
        collection = Collection.objects.create(name=collection_name)
        self.users = [
            User.objects.create(collection=collection, name=f"{username}_{i}")
            for i in range(4)
        ]
        self.ideas = [
            Idea.objects.create(
                title=f"title_{i}", user=self.users[0], collection=collection
            )
            for i in range(4)
        ]

    def test_create_vote_via_post(self, client):
        url = reverse("vote")
        data = {
            "idea_id": self.ideas[0].id,
            "user_id": self.users[0].id,
        }
        response = client.post(url, data)

        assert Vote.objects.count() == 1

    def test_dont_create_vote_via_get(self, client):
        url = reverse("vote")
        data = {
            "idea_id": self.ideas[0].id,
            "user_id": self.users[0].id,
        }
        with pytest.raises(ValueError) as exx:
            response = client.get(url, data)

        assert Vote.objects.count() == 0

    def test_like(self, client):
        url = reverse("vote")
        data = {
            "is_like": True,
            "idea_id": self.ideas[0].id,
            "user_id": self.users[0].id,
        }
        response = client.post(url, data)

        assert Vote.objects.filter(is_like=True).count() == 1

    def test_dislike(self, client):
        url = reverse("vote")
        data = {
            "is_like": False,
            "idea_id": self.ideas[0].id,
            "user_id": self.users[0].id,
        }
        response = client.post(url, data)

        assert Vote.objects.filter(is_like=False).count() == 1

    def test_reset_vote(self, client):
        for is_like in [True, False]:
            vote = Vote.objects.create(
                idea_id=self.ideas[0].id, user_id=self.users[0].id, is_like=is_like
            )
            assert Vote.objects.count() == 1

            url = reverse("vote")
            data = {
                "is_like": is_like,
                "idea_id": self.ideas[0].id,
                "user_id": self.users[0].id,
            }
            response = client.post(url, data)

            assert Vote.objects.count() == 1
            assert Vote.objects.first().is_like == None

            vote.delete()
