from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
import random
from .forms import TweetForm
from django.utils.http import is_safe_url
from django.conf import settings
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['POST'])  # the http method the client sent is POST
def tweet_create_view(request, *args, **kwargs):
    """
    DRF view response, serialized data being sent back.
    check for post request, raise error, user authentication check
    """
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    """
    DRF view response, serialized data being sent back.
    """
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    DRF view response, serialized data being sent back. Its a detail view sending content.
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)  # not found
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)  # found status


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html')


def tweet_create_view_pure_django(request, *args, **kwargs):
    """
    form for creating Tweet content. form can be initialized with or wothout data as shown in the first line.
    if data is being sent by post method then it will to form or None.
    Check for validation. 
    if validated save to db and initilze new form.
    """
    # if sent from ajax
    if not request.user.is_authenticated:
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    # TODO: if request is POST and from ajax validate and save data and return created instance
    if request.is_ajax() and request.method == "POST" and form.is_valid():
        # obj = Tweet.objects.all()
        # obj.delete()
        tweet_obj = form.save(commit=False)
        tweet_obj.user = request.user or None
        tweet_obj.save()
        return JsonResponse(tweet_obj.serialize(), status=201)
    if request.is_ajax() and form.errors:
        return JsonResponse(form.errors, status=400)
    next_url = request.POST.get('next') or None
    form.user = request.user or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Can be consumed by using any thing including JS, react, JAVA etc..
    return: Json response.
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response": tweets_list,
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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
