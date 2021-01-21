from django.contrib import admin
from .models import Tweet, TweetLikeUser


class TweetLikeUser(admin.TabularInline):
    model = TweetLikeUser


class TweetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    list_filter = ['user__username', 'user__email']
    inlines = [TweetLikeUser]

    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetAdmin)
