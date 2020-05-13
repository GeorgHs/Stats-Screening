

import unittest
from .. import Stock, Figure


class TestHelloWorld(unittest.TestCase):

	def test_equals(self):
		fig = Figure.objects.create()
		fig.figurename = "name1"
		self.assertEquals(fig.figurename,"name1")

	def test_secondTry(self):
		stock = Stock.objects.create()
		stock.ticker = "TKG"
		self.assertEquals(stock.ticker,"TKG")