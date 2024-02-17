from django import forms

from .models import Collection, Idea, User


class CollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields["name"].widget.attrs.update(autofocus="autofocus")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Collection
        fields = ["name"]

    def clean(self):
        if not self.cleaned_data.get("name"):
            raise forms.ValidationError("Name can't be empty")


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields["name"].widget.attrs.update(autofocus="autofocus")
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ["name"]
        collection_id = forms.CharField(widget=forms.HiddenInput())


class IdeaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields["title"].widget.attrs.update(autofocus="autofocus")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Idea
        fields = ["title", "description"]
