from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(
        upload_to="images/", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-id"]

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 500)
        }
