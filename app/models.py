from django.db import models


# Create your models here.

class News(models.Model):
    id = models.CharField(max_length=4294967295, primary_key=True)
    title = models.CharField(max_length=4294967295)
    date = models.CharField(max_length=4294967295)
    authors = models.CharField(max_length=4294967295)
    categories = models.CharField(max_length=4294967295)
    link = models.CharField(max_length=4294967295)
    text = models.CharField(max_length=4294967295)
    citation_rank = models.CharField(max_length=4294967295)
    rank = models.CharField(max_length=4294967295)
    likes = models.CharField(max_length=4294967295)

    class Meta:
       managed = False
       db_table = 'app_news'

