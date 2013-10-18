from django.contrib import admin

from .models import AppUser, AppUserMembership, Suggestion, SuggestionList, Algorithm

admin.site.register(AppUser)
admin.site.register(AppUserMembership)
admin.site.register(Suggestion)
admin.site.register(SuggestionList)
admin.site.register(Algorithm)
