from builtins import property, float
from typing import List
Portfolio = List[float]


class Chart():
    def __int__(self, ChartType, Timehorizon, portfolio):
        self.chartType = ChartType
        self.timeHorizon = Timehorizon
        #es kann immer nur einem Portfolio ein Chart zu ein und derselben Zeit zugeordnet werden!
        self.portfolio = portfolio
        #so far merely a pure performance chart is being displayed

    @property
    def chartType(self):
        return '{}'.format(self.chartType)

    @property
    def timeHorizon(self):
        return '{}'.format(self.timeHorizon)

    @property
    def portfolioName(self):
        return '{}'.format(self.portfolioName)

    @chartType.setter
    def chartType(self, type):
        self.chartType = type

    @chartType.deleter
    def chartType(self):
        self.chartType = None

    @timeHorizon.setter
    def timeHorizon(self, horizon):
        self.timeHorizon = horizon

    @timeHorizon.deleter
    def timeHorizon(self):
        self.timeHorizon = None

    @portfolioName.setter
    def portfolioName(self, portfolioName):
        self.portfolioName = portfolioName

    @portfolioName.deleter
    def portfolioName(self):
        self.portfolioName = None