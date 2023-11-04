from django.urls import path
from .views import BookListView, BookFormView, RateBookView, SearchRedictView, SearchBookView


urlpatterns = [
    path("", BookListView.as_view(), name="book_list_view"),
    path("<uuid:pk>/", BookFormView.as_view(), name="book_form_view"),
    path("<uuid:pk>/<user_id>", RateBookView.as_view(), name="rate_book_view"),
    path("search", SearchBookView.as_view(), name="search_book"),
]
