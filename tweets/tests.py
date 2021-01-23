from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from rest_framework.test import APIClient

User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="PP", password="admin")
        tweet_obj = Tweet.objects.create(content="my Tweet", user=self.user)

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="my Tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 2)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="admin")
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        print(response.json())
