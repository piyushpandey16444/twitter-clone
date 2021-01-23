from django.contrib import admin
from django.urls import path
from tweets.views import (home_view, tweet_detail_view, tweet_delete_view, tweet_action_view,
                          tweet_list_view, tweet_create_view)

"""
Base ENDPOINT  /api/tweets/
"""

urlpatterns = [
    path('', tweet_list_view, name='tweets'),
    path('action/', tweet_action_view, name="tweet-action-view"),
    path('create/', tweet_create_view, name="create-tweet"),
    path('<int:tweet_id>/', tweet_detail_view, name="tweet-detail-view"),
    path('<int:tweet_id>/delete/', tweet_delete_view, name="tweet-delete-view"),
]
