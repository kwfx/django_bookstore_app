from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, Review


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

    def get(self, request, *args, **kwargs):
        res= super().get(request, *args, **kwargs)
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
