from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:date>", views.specific_date, name="specific_date"),
    path("<str:date>/<str:category>", views.specific_category, name="specific_category")
]

