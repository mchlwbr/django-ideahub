from django.db import models
from django.db.models import Case, Count, Value, When


class Collection(models.Model):
    name = models.CharField(
        max_length=255,
        primary_key=True,
        verbose_name="Collection Name",
        help_text="Name of the collection you want to access (e.g. 'Brainstorming' or 'London')",
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Username",
        help_text="Your username",
    )
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(User, self).save(*args, **kwargs)


class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    total_likes = models.IntegerField(default=0, editable=False)
    total_dislikes = models.IntegerField(default=0, editable=False)
    score = models.IntegerField(default=0, editable=False)

    class Meta:
        unique_together = ("title", "collection")

    def fetch_likes(self):
        likes, dislikes = self.vote_set.aggregate(
            likes=Count(Case(When(is_like=True, then=Value(1)))),
            dislikes=Count(Case(When(is_like=False, then=Value(1)))),
        ).values()
        self.total_likes = likes
        self.total_dislikes = dislikes
        self.score = likes - dislikes


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    is_like = models.BooleanField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("user", "idea", name="vote_constraint"),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.idea.fetch_likes()
        self.idea.save()
