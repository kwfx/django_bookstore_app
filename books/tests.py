from django.test import TestCase
from .models import Book, Review
from django.contrib.auth import get_user_model
from django.urls import reverse


class BooksTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.book = Book.objects.create(
            title="Harry Potter",
            author="JK Rowling",
            price="25.00",
        )
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
        )

        cls.review = Review.objects.create(
            book=cls.book,
            user=cls.user,
            text="An excellent review",
            rate=4
        )

    def testBookListing(self):
        self.assertEqual(f"{self.book.title}", "Harry Potter")
        self.assertEqual(f"{self.book.author}", "JK Rowling")
        self.assertEqual(f"{self.book.price}", "25.00")

    def testBooklistView(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        # self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "books/book_detail.html")
