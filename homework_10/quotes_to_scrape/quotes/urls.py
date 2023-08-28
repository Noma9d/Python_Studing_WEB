from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:page>", views.main, name="main_pagin"),
    path("author/<str:author_name>", views.author, name="author"),
    path("quote/", views.quote, name="quote"),
    path("author_create/", views.author_create, name="author_create"),
]
