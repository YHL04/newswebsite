from django.db import models


# Create your models here.

class News(models.Model):
    id = models.CharField(max_length=1_000_000, primary_key=True)
    title = models.CharField(max_length=1_000_000)
    date = models.CharField(max_length=1_000_000)
    authors = models.CharField(max_length=1_000_000)
    categories = models.CharField(max_length=1_000_000)
    link = models.CharField(max_length=1_000_000)
    text = models.CharField(max_length=1_000_000)
    citation_rank = models.CharField(max_length=1_000_000)
    rank = models.CharField(max_length=1_000_000)
    likes = models.CharField(max_length=1_000_000)

    class Meta:
       managed = False
       db_table = 'app_news'

