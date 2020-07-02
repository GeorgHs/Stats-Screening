#subclass of stock and chart!
from .Stock import Stock
from .Figure import Figure
from .Chart import Chart

class Toolbox():
    def __init__(self, figureDict = None, chartDict = None):
        # set up dict
        if self.figureDict is None:
            self.figureDict = {  # key, #value
                '': '',
            }
        else:
            self.figureDict = figureDict

        if self.chartDict is None:
            self.chartDict = {  # key, #value
                '': '',
            }
        else:
            self.chartDict = chartDict

    def addFigure(self, figure: Figure):
        self.figureDict[figure.figurename()] = figure

    def removeFigure(self, figure: Figure):
        #create for each which finds the specified Stock and then removes it
        del self.figureDict[figure.figurename()]

    def getFigure(self, figure):
        ##enter name and then find Stock and return it's object
        return self.figureDict[figure.figurename()]


    def addChart(self, chart: Chart):
        self.chartDict[chart.portfolioName] = chart

    def removeChart(self, chart: Chart):
        # create for each which finds the specified Stock and then removes it
        del self.chartDict[chart.portfolioName]

    def getChart(self, portfolioName):
        ##enter name and then find Stock and return it's object
        return self.chartDict[portfolioName]

