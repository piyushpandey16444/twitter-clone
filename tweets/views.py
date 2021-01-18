from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
import random
from .forms import TweetForm
from django.utils.http import is_safe_url
from django.conf import settings

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html')


def tweet_create_view(request, *args, **kwargs):
    """
    form for creating Tweet content. form can be initialized with or wothout data as shown in the first line.
    if data is being sent by post method then it will to form or None.
    Check for validation. 
    if validated save to db and initilze new form.
    """
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Can be consumed by using any thing including JS, react, JAVA etc..
    return: Json response.
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content,
                    "likes": random.randint(0, 50)} for x in qs]
    data = {
        "response": tweets_list,
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Can be consumed by using any thing including JS, react, JAVA etc..
    return: Json response.
    """
    data = {
        "id": tweet_id,
        # "image": tweet_obj.image
    }
    status = 200
    try:
        tweet_obj = Tweet.objects.get(id=tweet_id)
        data['content'] = tweet_obj.content
    except:
        data['message'] = "Not Found"
        status = 404
        # raise Http404

    # json.dumps content_type=application/json
    return JsonResponse(data, status=status)
    # return HttpResponse(f"<h1>Hello {tweet_id}-{tweet_obj}</h1")
