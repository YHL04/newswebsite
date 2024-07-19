from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta

from .models import News, User
from .scraper import arxiv_scraper


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
    try:
        email = str(request.user.email)
        user = User(user_id=email)
        user.save()
    except Exception as e:
        pass

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


def memes(request):
    template = loader.get_template("memes.html")
    context = {}
    return HttpResponse(template.render(context, request))


def liked(request):
    try:
        email = str(request.user.email)
        user = User(user_id=email)
        news_data = user.likes.all()
    except Exception as e:
        news_data = []

    template = loader.get_template("liked.html")
    context = {
        "news_data": zip(news_data, check_liked(request, news_data)),
    }
    return HttpResponse(template.render(context, request))


def search(request):
    news_data = []
    if request.POST.get('search-bar') is not None:
        news_data = News.objects.filter(title__icontains=request.POST.get('search-bar').replace("\n", "").replace("\r", ""))
        news_data = news_data.order_by('-citation_rank')

    template = loader.get_template("search.html")
    context = {
        "news_data": zip(news_data, check_liked(request, news_data)),
    }
    return HttpResponse(template.render(context, request))


def arxiv(request):
    news_data = []
    if request.POST.get('search-bar') is not None:
        news_data_ = arxiv_scraper(request.POST.get('search-bar').replace("\n", "").replace("\r", ""), max_results=10)
        news_data = []
        for news_ in news_data_:
            news = News(news_id=str(news_['id']), title=str(news_['title']),
                        date=str(news_['date']), authors=str(news_['authors']),
                        categories=str(news_['categories']), link=str(news_['link']),
                        text=str(news_['text']), affiliations=str(news_['affiliations']),
                        citation_rank=str(news_['citation_rank']), final_rank=str(news_['final_rank']),
                        like_count=str(news_['like_count']))
            news.save()
            news_data.append(news)

    template = loader.get_template("arxiv.html")
    context = {
        "news_data": zip(news_data, check_liked(request, news_data)),
    }
    return HttpResponse(template.render(context, request))


def stats(request):
    template = loader.get_template("stats.html")
    t_val = [860, 1140, 1060, 1060, 1070, 1110, 1330, 2210, 7830, 2478]
    d_val = [1600, 1700, 1700, 1900, 2000, 2700, 4000, 5000, 6000, 7000]
    r_val = [300, 700, 2000, 5000, 6000, 4000, 2000, 1000, 200, 100]

    # Set all dates to empty list except for the first and last one
    x_val = ['2021-11-06' for _ in t_val]
    month = LatestToday().date.strftime('%b').upper()

    context = {
        "x_values": x_val,
        "transformer_values": t_val,
        "diffusion_values": d_val,
        "rl_values": r_val,
    }
    return HttpResponse(template.render(context, request))


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
        post_obj_news = get_object_or_404(News, news_id=post_id)
        post_obj_users = get_object_or_404(User, user_id=email)

        user = User(user_id=email)
        news = News(news_id=post_id)

        if post_obj_news.likes.filter(user_id=email).exists():
            if news.like_count is None: news.like_count = 0
            news.like_count = str(int(news.like_count) - 1)

            user.save()
            news.save()

            post_obj_news.likes.remove(user)
            post_obj_news.save()

            post_obj_users.likes.remove(news)
            post_obj_users.save()

            flag = False
        else:
            if news.like_count is None: news.like_count = 0
            news.like_count = str(int(news.like_count) + 1)

            user.save()
            news.save()

            post_obj_news.likes.add(user)
            post_obj_news.save()

            post_obj_users.likes.add(news)
            post_obj_users.save()

            # if news.like_count is None: news.like_count = 0
            # news.like_count = str(int(news.like_count) + 1)

            flag = True

        new_string = "Likes: {}".format(post_obj_news.total_likes)
        return JsonResponse({"new_string": new_string, "flag": flag})

    return HttpResponse("Error")

