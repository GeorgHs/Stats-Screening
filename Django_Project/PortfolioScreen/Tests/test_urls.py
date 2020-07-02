from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import PortfolioScreen,about,chart,table,settings

class TestClass(SimpleTestCase):

    def test_main_url_is_resolved(self):
        url = reverse('PortfolioScreen')
        print(resolve(url))
        self.assertEquals(resolve(url).func, PortfolioScreen)

    def test_about_url_is_resolved(self):
        url = reverse('about')
        print(resolve(url))
        self.assertEquals(resolve(url).func, about)

    def test_table_url_is_resolved(self):
        url = reverse('portfolio-table')
        print(resolve(url))
        self.assertEquals(resolve(url).func, table)


    def test_chart_url_is_resolved(self):
        url = reverse('portfolio-chart')
        print(resolve(url))
        self.assertEquals(resolve(url).func, chart)

    def test_settings_url_is_resolved(self):
        url = reverse('portfolio-settings')
        print(resolve(url))
        self.assertEquals(resolve(url).func, settings)