from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta

from .models import News, User


class LatestToday:
    """
    If today is weekends and there is no papers that day, decrement latest today by one
    until a max decrement of 5 days. This makes it so that the first page of the website
    will always contain content or if the database is empty, stop decrementing after 5.
    """
    def __init__(self):
        latest = News.objects.latest('date')

        print(latest.title)
        print(latest.date)

        if latest.date is None:
            self.date = datetime.today()
        else:
            self.date = latest.date


def daily_paper_render(request, date, latest_today, category="none", categories=None):
    news_data = News.objects.filter(date__range=[date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')])
    news_data = news_data.order_by('-citation_rank')

    if category != "none":

        news_data_ = []
        for news in news_data:

            if any(s in news.text.lower() for s in categories[category]):
                if category != "other":
                    news_data_.append(news)

            else:
                if category == "other":
                    news_data_.append(news)

        news_data = news_data_

    curr_date = date
    prev_date = date - timedelta(days=1)
    next_date = date + timedelta(days=1)

    if next_date > latest_today:
        next_date = latest_today
        next = False
    else:
        next_date = next_date
        next = True

    month = date.strftime('%b').upper()
    day = date.strftime('%d')

    template = loader.get_template("news.html")
    context = {
        "news_data": zip(news_data, check_liked(request, news_data)),
        "curr_date": curr_date.strftime('%Y-%m-%d'),
        "prev_date": prev_date.strftime('%Y-%m-%d'),
        "next_date": next_date.strftime('%Y-%m-%d'),
        "month": month,
        "day": day,
        "next": next,
        "category": category,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    return daily_paper_render(request, date=LatestToday().date, latest_today=LatestToday().date)


def specific_date(request, date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except Exception as e:
        return HttpResponse("")

    return daily_paper_render(request, date=date, latest_today=LatestToday().date)


def specific_category(request, date, category):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except Exception as e:
        return HttpResponse("")

    categories = {"transformer": ["transformer", "llm", "gpt", "tokenizer"],
                  "diffusion": ["diffusion", "ddpm"],
                  "reinforcement": ["reinforcement", "atari"],
                  "other": ["transformer", "llm", "gpt", "tokenizer", "diffusion",
                            "ddpm", "reinforcement", "atari"]}

    return daily_paper_render(request, date=date, latest_today=LatestToday().date, category=category, categories=categories)


def about(request):
    template = loader.get_template("about.html")
    context = {}
    return HttpResponse(template.render(context, request))


def check_liked(request, news_data):
    liked = [False for _ in news_data]

    # check if user is authenticated
    try:
        email = str(request.user.email)
    except Exception as e:
        return liked

    for i, news in enumerate(news_data):
        if news.likes.filter(user_id=email).exists():
            liked[i] = True

    # user = get_object_or_404(User, user_id=email)
    # liked_news = user.likes.objects.all()
    #
    # for i, news in enumerate(news_data):
    #     if news in liked_news:
    #         liked[i] = True

    return liked


def post_like(request):
    try:
        email = str(request.user.email)
    except Exception as e:
        return JsonResponse({"new_string": "Login Required", "flag": True})

    if request.method == 'GET':
        post_id = request.GET['post_id']
        post_obj = get_object_or_404(News, news_id=post_id)

        if post_obj.likes.filter(user_id=email).exists():
            user = User(user_id=email)
            user.save()
            post_obj.likes.remove(user)
            post_obj.save()
            flag = False
        else:
            user = User(user_id=email)
            user.save()
            post_obj.likes.add(user)
            post_obj.save()
            flag = True

        new_string = "Likes: {}".format(post_obj.total_likes)
        return JsonResponse({"new_string": new_string, "flag": flag})

    return HttpResponse("Error")

