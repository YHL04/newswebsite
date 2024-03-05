from django.http import HttpResponse
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
        dates = [datetime.strptime(news.date.split()[0], '%Y-%m-%d') for news in news_data]
        dates.sort(key=lambda x: x.date)
        self.date = dates[-1]


latesttoday = LatestToday()


def daily_paper_render(request, date):
    news_data = News.objects.all()

    for news in news_data:
        news.date = news.date.split()[0]
        news.citation_rank = round(float(news.citation_rank), 2)

    news_data = [news for news in news_data if datetime.strptime(news.date, '%Y-%m-%d') == date]
    news_data.sort(key=lambda x: -x.citation_rank)

    curr_date = date.strftime('%Y-%m-%d')
    prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = date + timedelta(days=1)

    if next_date > latesttoday.date:
        next_date = latesttoday.date.strftime('%Y-%m-%d')
        next = False
    else:
        next_date = next_date.strftime('%Y-%m-%d')
        next = True

    month = date.strftime('%b').upper()
    day = date.strftime('%d')

    template = loader.get_template("news.html")
    context = {
        "news_data": news_data,
        "curr_date": curr_date,
        "prev_date": prev_date,
        "next_date": next_date,
        "month": month,
        "day": day,
        "next": next
    }
    return HttpResponse(template.render(context, request))


def index(request):
    return daily_paper_render(request, latesttoday.date)


def specific_date(request, date):
    if date == "favicon.ico":
        # not sure why it goes to /favicon.ico but return nothing
        # so it returns back to original page
        return HttpResponse("")
    date = datetime.strptime(date, '%Y-%m-%d')
    return daily_paper_render(request, date)

