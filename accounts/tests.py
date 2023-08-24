from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .forms import CustomUserCreationForm
# from .views import SignupPageView


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testUser",
            password="TestUser8520",
            email="test@test.com"
        )
        self.assertEqual(user.username, "testUser")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="superUser",
            password="superUser8520",
            email="testsuper@test.com"
        )
        self.assertEqual(user.username, "superUser")
        self.assertEqual(user.email, "testsuper@test.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class SignUpTests(TestCase):

    username = "test8521"
    email = "test8521@test.com"

    def setUp(self) -> None:
        self.url = reverse("account_signup")
        self.response = self.client.get(self.url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")
    
    def test_signup_form(self):
        form = self.response.context.get("form")
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        # self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, "csrfmiddlewaretoken")
    
    # def test_signup_view(self):
    #     view = resolve(self.url)
    #     self.assertEqual(view.func.__name__, SignupPageView.as_view().__name__)
