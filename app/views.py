from django.http import HttpResponse, JsonResponse
from django.template import loader

from datetime import datetime, timedelta

from .models import News


class LatestToday:
    """
    If today is weekends and there is no papers that day, decrement latest today by one
    until a max decrement of 5 days. This makes it so that the first page of the website
    will always contain content or if the database is empty, stop decrementing after 5.
    """
    def __init__(self):
        news_data = News.objects.all()

        # get all dates in datetime format
        dates = [datetime.strptime(news.date.split()[0], '%Y-%m-%d') for news in news_data]

        # get max date
        if len(dates) == 0:
            self.date = datetime.today()
        else:
            self.date = max(dates)


def daily_paper_render(request, date, latest_today, category="none", categories=None):
    news_data = News.objects.all()

    for news in news_data:
        news.date = news.date.split()[0]
        news.citation_rank = round(float(news.citation_rank), 2)

    news_data = [news for news in news_data if datetime.strptime(news.date, '%Y-%m-%d') == date]
    news_data.sort(key=lambda x: -x.citation_rank)

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
        "news_data": news_data,
        "curr_date": curr_date.strftime('%Y-%m-%d'),
        "prev_date": prev_date.strftime('%Y-%m-%d'),
        "next_date": next_date.strftime('%Y-%m-%d'),
        "month": month,
        "day": day,
        "next": next,
        "category": category
    }
    return HttpResponse(template.render(context, request))


def index(request):
    return daily_paper_render(request, date=LatestToday().date, latest_today=LatestToday().date)


def specific_date(request, date):
    if date == "favicon.ico":
        # not sure why it goes to /favicon.ico but return nothing
        # so it returns back to original page
        return HttpResponse("")

    if date.endswith(".txt"):
        return HttpResponse("")

    if date == "about":
        return about(request)

    date = datetime.strptime(date, '%Y-%m-%d')
    return daily_paper_render(request, date=date, latest_today=LatestToday().date)


def specific_category(request, date, category):
    if date == "favicon.ico":
        # not sure why it goes to /favicon.ico but return nothing
        # so it returns back to original page
        return HttpResponse("")

    if date.endswith(".txt"):
        return HttpResponse("")

    if date == "about":
        return about(request)

    categories = {"transformer": ["transformer", "llm", "gpt", "tokenizer"],
                  "diffusion": ["diffusion", "ddpm"],
                  "reinforcement": ["reinforcement", "atari"],
                  "other": ["transformer", "llm", "gpt", "tokenizer", "diffusion",
                            "ddpm", "reinforcement", "atari"]}

    date = datetime.strptime(date, '%Y-%m-%d')
    return daily_paper_render(request, date=date, latest_today=LatestToday().date, category=category, categories=categories)


def about(request):
    template = loader.get_template("about.html")
    context = {}
    return HttpResponse(template.render(context, request))


def post_like(request):
    total_likes = 0
    flag = True

    return JsonResponse({"total_likes": total_likes, "flag": flag})