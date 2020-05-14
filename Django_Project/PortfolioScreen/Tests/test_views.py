from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):


    def test_project_about_GET(self):
        client = Client()
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PortfolioScreen/about.html')
