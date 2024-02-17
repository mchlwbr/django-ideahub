from django import template

from ideahub.models import Idea, User

register = template.Library()


@register.simple_tag
def users_vote(idea: Idea, user: User):
    try:
        return idea.vote_set.get(user=user).is_like
    except Exception:
        return None
