from django.contrib import admin

from .models import Poll, Vote, Choice, PollAllowedUser


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'type')
    raw_id_fields = ('creator',)
    list_filter = ('is_active', 'type', 'start_time', 'end_time')
    search_fields = ('title', 'description')
    radio_fields = {
        'type': admin.HORIZONTAL
    }


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'choice')
    raw_id_fields = ('user', 'poll', 'choice')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('poll', 'text', 'votes_count')
    raw_id_fields = ('poll', )
    search_fields = ('text', )


@admin.register(PollAllowedUser)
class PollAllowedUserAdmin(admin.ModelAdmin):
    list_display = ('poll', 'user')
    raw_id_fields = ('poll', 'user')