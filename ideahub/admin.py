from django.contrib import admin

from .models import Collection, Idea, User, Vote


class CollectionAdmin(admin.ModelAdmin):
    pass


class IdeaAdmin(admin.ModelAdmin):
    pass


class VoteAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(User, UserAdmin)
