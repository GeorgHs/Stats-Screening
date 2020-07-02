from django.test import TestCase
from ..Portfolio import Portfolio
from ..Figure import Figure
from ..Stock import Stock
from ..Chart import Chart
from ..Toolbox import Toolbox


class TestModels(TestCase):

    allstocks = {'':''}

    def setUp(self):
        self.portfolio1 = Portfolio(
            'Portfolio',
            '02-02-2015',
        )
        stock1 = Stock('TSLA','725')
        stock1.addfigure(
            Figure('Alpha','x/a','12'))
        self.allstocks["TSLA"] = stock1
        self.portfolio1.addStock(stock1)

        stock2 = Stock('APC','282')
        stock2.addfigure(
            Figure('Beta','x/b','13')
        )
        self.allstocks["APC"] = stock2
        self.portfolio1.addStock(stock2)


    def test_whether_stock_append_to_portfolio(self):
        self.assertDictEqual(self.portfolio1.stockList,self.allstocks)

    def test_whether_stock_ticker_is_in_portfolio(self):
        self.assertEqual(self.portfolio1.getStock('APC').ticker,'APC')
