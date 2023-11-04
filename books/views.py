from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, Review
from django.http import HttpResponseRedirect
from django.db.models import Q



class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "book_list" # object_list in template => book_list
    template_name = "books/book_list.html"
    ordering = ['title']
    login_url = "account_login"


class BookFormView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = "books/book_detail.html"
    login_url = "account_login"
    permission_required = "books.special_status"
    queryset = Book.objects.all().prefetch_related('reviews__author',)

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        self.object.user = request.user
        return res


class RateBookView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        r = int(self.request.POST.get("button_star")[0])
        user_id = kwargs["user_id"]
        book = get_object_or_404(Book, pk=kwargs["pk"])
        if user_id != "None":
            user = get_user_model().objects.get(id=user_id)
            rev = book.reviews.all().filter(user__id=user_id)
            if rev:
                current_rate = rev[0].rate
                if current_rate == 1 and r == 1:
                    r = 0
                rev[0].rate = r
                rev[0].save()
            else:
                Review.objects.create(
                    book=book,
                    rate=r,
                    text="No text",
                    user=user
                )
        return reverse("book_form_view", args=[book.id])


class SearchRedictView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        title = self.request.POST.get("search_input")
        books = Book.objects.all().filter(title=title)
        if not books:
            return f"{reverse('book_list_view')}?not_found=1"
        return reverse("book_form_view", args=[books[0].id])


class SearchBookView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_search.html"
    # queryset = Book.objects.filter(title__icontains="beginners")

    def get_queryset(self) -> QuerySet[Any]:
        search_query = self.request.GET.get("q")
        print("search query ::::::::::::: ", search_query)
        return self.model.objects.all().filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
