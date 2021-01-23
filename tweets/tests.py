from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from rest_framework.test import APIClient

User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="PP", password="admin")
        self.userb = User.objects.create_user(username="AP", password="adminb")
        tweet_obj = Tweet.objects.create(content="my Tweet1", user=self.user)
        tweet_obj2 = Tweet.objects.create(content="my Tweet2", user=self.userb)
        tweet_obj = Tweet.objects.create(content="my Tweet3", user=self.userb)
        self.current_count = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="my Tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="admin")
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        like_count = response.data.get('likes')
        self.assertEqual(like_count, 1)
        self.assertEqual(response.status_code, 200)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "unlike"})
        like_count = response.data.get('likes')
        self.assertEqual(like_count, 0)
        self.assertEqual(response.status_code, 200)

    def test_action_retweet(self):
        client = self.get_client()
        current_count = self.current_count
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_api_view(self):
        client = self.get_client()
        current_count = self.current_count
        request_data = {"content": "This is test case tweet !"}
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 204)
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/tweets/2/delete/")
        self.assertEqual(response.status_code, 404)
