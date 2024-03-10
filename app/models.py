from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=1_000_000, unique=True, primary_key=True)

    class Meta:
        managed = False
        db_table = 'app_user'


class News(models.Model):
    news_id = models.CharField(max_length=1_000_000, unique=True, primary_key=True)
    title = models.CharField(max_length=1_000_000, unique=False)
    date = models.CharField(max_length=1_000_000, unique=False)
    authors = models.CharField(max_length=1_000_000, unique=False)
    categories = models.CharField(max_length=1_000_000, unique=False)
    link = models.CharField(max_length=1_000_000, unique=False)
    text = models.CharField(max_length=1_000_000, unique=False)
    citation_rank = models.CharField(max_length=1_000_000, unique=False)
    final_rank = models.CharField(max_length=1_000_000, unique=False)
    likes = models.ManyToManyField(User, related_name='user_like', blank=True)

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
