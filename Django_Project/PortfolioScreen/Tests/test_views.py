from django.test import TestCase, Client
from django.urls import reverse
import unittest

class TestViews(TestCase):


    def test_project_about_GET(self):
        client = Client()
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PortfolioScreen/about.html')

if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))