from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=1_000_000, unique=False)
    date = models.CharField(max_length=1_000_000, unique=False)
    authors = models.CharField(max_length=1_000_000, unique=False)
    categories = models.CharField(max_length=1_000_000, unique=False)
    link = models.CharField(max_length=1_000_000, unique=True)
    text = models.CharField(max_length=1_000_000, unique=False)
    citation_rank = models.CharField(max_length=1_000_000, unique=False)
    final_rank = models.CharField(max_length=1_000_000, unique=False)
    likes = models.CharField(max_length=1_000_000, unique=False)

    class Meta:
       managed = False
       db_table = 'app_news'

