from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView, AboutPageView


class HomePageTest(SimpleTestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_home_page_url(self):
        # response = self.client.get("/")
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "HOME")
    
    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_homepage_url_resolves_homepageview(self): # new
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTest(SimpleTestCase):

    def setUp(self) -> None:
        self.url = reverse("about")
        self.response = self.client.get(self.url)
        return super().setUp()

    def test_aboutpage_responsecode(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_tpml(self):
        self.assertTemplateUsed(self.response, "about.html")

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "This is our first django app")

    def test_aboutpage_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)