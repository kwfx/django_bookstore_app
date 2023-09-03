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

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book_form_view", args=[self.id])
    
    @property
    def overall_rate(self):
        return self.reviews.aggregate(overall_rate=models.Avg("rate"))["overall_rate"]


class Review(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField("Review")
    rate = models.IntegerField("Rate")

    def __str__(self) -> str:
        return f"The user : {self.user.username} / Book: {self.book.title} / Rate: {self.rate}"