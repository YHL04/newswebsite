from django.db import models


# Create your models here.

class News(models.Model):
    id = models.CharField(max_length=int(1e20), primary_key=True)
    title = models.CharField(max_length=int(1e20))
    date = models.CharField(max_length=int(1e20))
    authors = models.CharField(max_length=int(1e20))
    categories = models.CharField(max_length=int(1e20))
    link = models.CharField(max_length=int(1e20))
    text = models.CharField(max_length=int(1e20))
    citation_rank = models.CharField(max_length=int(1e20))
    rank = models.CharField(max_length=int(1e20))
    likes = models.CharField(max_length=int(1e20))

    class Meta:
       managed = False
       db_table = 'app_news'

