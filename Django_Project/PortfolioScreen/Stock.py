from builtins import property, type, set


class Stock():

    def __init__(self, tickerValue, priceValue, figuresValue=None):
        self._ticker = tickerValue
        self._curr_price = priceValue
        if figuresValue is None:
            self._figures = {  # key, #value '': '', }
            
        else: self._figures = figuresValue

    def calcAllFigures(self):
        for item in self._figures.items():
        print(item)
        print(type(item))

    def addfigure(self, figure):
        name_figure = figure.figurename
        self._figures[name_figure] = figure

    def removefigure(self, figurename):
        del self._figures[figurename]

    def getfigure(self, figurename):
        return ''.format(self._figures[figurename])



    @property
    def ticker(self):
        return '{}'.format(self._ticker)

    @ticker.setter
    def ticker(self, value):
        self._ticker = value

    @ticker.deleter
    def ticker(self):
        self.ticker = None



    @property
    def curr_price(self):
        return '{}'.format(self._curr_price)

    @curr_price.setter
    def curr_price(self, value):
        self._curr_price = value



    @curr_price.deleter
    def TimeHorizon(self):
        self.curr_price = None
