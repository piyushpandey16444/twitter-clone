from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 240


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        """
        check for length of the Tweet, should not be grater than 240 i.e 
        specified limit.
        """
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This Tweet is too long !")
        return content
