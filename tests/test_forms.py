import pytest

from ideahub.forms import CollectionForm


class TestCollectionForm:
    def test_name_cant_be_empty(self):
        form = CollectionForm(data={"name": ""})
        assert not form.is_valid()
        assert "This field is required." in form.errors["name"]
