from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
import math

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to="covers/", blank=True)

    orderby = "id"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_form_view", args=[self.id])

    def get_next_record(self):
        all_recs = Book.objects.all().order_by(self.orderby)
        if not all_recs: return
        next_records = all_recs.filter(id__gt=self.__dict__.get(self.orderby))
        if next_records:
            return reverse("book_form_view", args=[next_records.first().id])
        else:
            return reverse("book_form_view", args=[all_recs.first().id])

    def get_previous_record(self):
        all_recs = Book.objects.all().order_by(f"-{self.orderby}")
        if not all_recs:
            return
        next_records = all_recs.filter(id__lt=self.__dict__.get(self.orderby))
        if next_records:
            return reverse("book_form_view", args=[next_records[0].id])
        return reverse("book_form_view", args=[all_recs.first().id])

    @property
    def overall_rate(self):
        return self.reviews.aggregate(overall_rate=models.Avg("rate"))["overall_rate"]

    @property
    def current_user_rate(self):
        if self.user.is_authenticated:
            user_rev = self.reviews.filter(user=self.user)
            return self.reviews.filter(user=self.user)[0].rate if user_rev else 0
        return 0


# class ReviewManager(models.Manager):
#     def review_list(self, User):
#         list = Review.objects.filter(user=User)
#         return list


class Review(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField("Review")
    rate = models.IntegerField("Rate")
    # objects = ReviewManager()

    def __str__(self) -> str:
        return f"The user : {self.user.username} / Book: {self.book.title} / Rate: {self.rate}"
