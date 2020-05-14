from builtins import property, type, set

#subclass of Stock

class Portfolio():

    def __init__(self, portfolioNameValue = "Portfolio", inceptionDateValue = '01-01-2015', stockListvalue = None, figureListvalue = None, chartTypevalue = None):
        self._portfolioName = portfolioNameValue
        self._inceptionDate = inceptionDateValue
        self._chartType = chartTypevalue

        #set up dict
        if stockListvalue is None:
            self._stockList = {  # key, #value
                '': '',
            }
        else:
            self._stockList = stockListvalue

        if figureListvalue is None:
            self._figureList = {  # key, #value
                '': '',
            }
        else:
            self._figureList = figureListvalue


    # nur Stock-Objekt rein
    def addStock(self, stock):
        name_stock = stock.ticker
        self._stockList[name_stock] = stock

    # nur Stock-Objekt rein
    def removeStock(self, stock):
        #create for each which finds the specified Stock and then removes it
        del self._stockList[stock.ticker]

    def getStock(self, ticker):
        #enter name and then find Stock and return it's object
        return self._stockList[ticker]


    # hier darf nur das object Figure eingefügt werden
    def addfigure(self, figure):
        self.stockList[figure.figurename()] = figure
    # hier darf nur das object Figure eingefügt werden
    def removefigure(self, figure):
        #create for each which finds the specified Stock and then removes it
        del self.stockList[figure.figurename()]

    def getfigure(self, figureid = None, figurename = None):
        if figureid is None and figurename is not None:

            return '{}'.format(self.figureList[figurename])
        elif figurename is None and figureid is not None:
            # hier ist noch was zu tun
            return "noch nicht fertig"
        elif figurename is None and figureid is None:
            return None

    @property
    def portfolioName(self):
        return '{}'.format(self._portfolioName)


    @portfolioName.setter
    def portfolioName(self, value):
        self._portfolioName = value


    @property
    def inceptionDate(self):
        return '{}'.format(self._inceptionDate)

    @inceptionDate.setter
    def inceptionDate(self, value):
        self._inceptionDate = value


    @property
    def stockList(self):
        return self._stockList

    @stockList.setter
    def stockList(self, value):
        self._stockList = value


    @property
    def figureList(self):
        return '{}'.format(self._figureList)

    @figureList.setter
    def figureList(self, value):
        self._figureList = value

    @property
    def chartType(self):
        return '{}'.format(self._chartType)

    @chartType.setter
    def chartType(self, value):
        self._chartType = value




