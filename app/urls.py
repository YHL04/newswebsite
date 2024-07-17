from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('allauth.socialaccount.urls')),
    path("memes/", views.memes, name="memes"),
    path("liked/", views.liked, name="liked"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("like/", views.post_like, name="post_like"),
    path("<str:date>/", views.specific_date, name="specific_date"),
    path("<str:date>/<str:category>/", views.specific_category, name="specific_category"),
]

