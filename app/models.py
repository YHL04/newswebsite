from django.db import models


class Stats(models.Model):
    stats_id = models.DateField(max_length=1_000_000, unique=True, primary_key=True)
    like_count = models.IntegerField(unique=False)
    transformers_count = models.IntegerField(unique=False)
    diffusion_count = models.IntegerField(unique=False)
    rl_count = models.IntegerField(unique=False)
    relevance = models.FloatField(unique=False)

    class Meta:
        managed = False
        db_table = 'app_stats'


class User(models.Model):
    user_id = models.CharField(max_length=1_000_000, unique=True, primary_key=True)
    likes = models.ManyToManyField('News', related_name='user_like', blank=True)

    class Meta:
        managed = False
        db_table = 'app_user'


class News(models.Model):
    news_id = models.CharField(max_length=1_000_000, unique=True, primary_key=True)
    title = models.CharField(max_length=1_000_000, unique=False)
    date = models.DateField(max_length=1_000_000, unique=False)
    authors = models.CharField(max_length=1_000_000, unique=False)
    categories = models.CharField(max_length=1_000_000, unique=False)
    link = models.CharField(max_length=1_000_000, unique=False)
    text = models.CharField(max_length=1_000_000, unique=False)
    affiliations = models.CharField(max_length=1_000_000, unique=False)
    citation_rank = models.FloatField(unique=False)
    final_rank = models.FloatField(unique=False)
    likes = models.ManyToManyField('User', related_name='news_like', blank=True)
    like_count = models.IntegerField(unique=False)

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
       managed = False
       db_table = 'app_news'


"""
date_joined
email
emailaddress
first_name
groups
id
is_active
is_staff
is_superuser
last_login
last_name
logentry
password
socialaccount
user_like
user_permissions
username
"""
