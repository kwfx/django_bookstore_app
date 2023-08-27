from django.urls import path
from .views import BookListView, BookFormView


urlpatterns = [
    path("", BookListView.as_view(), name="book_list_view"),
    path("<uuid:pk>/", BookFormView.as_view(), name="book_form_view"),
]
